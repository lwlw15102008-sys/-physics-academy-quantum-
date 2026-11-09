"""Shared drawing toolkit for the procedural asset generators (PIL + numpy only)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def out(*parts):
    p = os.path.join(ROOT, *parts); os.makedirs(os.path.dirname(p), exist_ok=True); return p
def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def C(h, a=255): return hexrgb(h) + (a,)
def save_webp(im, *parts, q=80): im.convert("RGB").save(out(*parts), quality=q, method=6)
def save_png(im, *parts): im.save(out(*parts), optimize=True)
def font(size): return ImageFont.truetype(FONT, int(size))

# ───────── gradients / backgrounds ─────────
def gradient(w, h, stops, mode="v"):
    if mode == "v": t = np.linspace(0, 1, h)[:, None] * np.ones((1, w))
    elif mode == "h": t = np.linspace(0, 1, w)[None, :] * np.ones((h, 1))
    else: t = (np.linspace(0, 1, w)[None, :] + np.linspace(0, 1, h)[:, None]) / 2
    n = len(stops) - 1
    cols = np.stack([np.array(hexrgb(s) if isinstance(s, str) else s, np.float32) for s in stops])
    pos = t * n; i = np.clip(np.floor(pos).astype(int), 0, n - 1); f = (pos - i)[..., None]
    return Image.fromarray((cols[i] * (1 - f) + cols[i + 1] * f).astype(np.uint8), "RGB")

def noise_field(rng, w, h, scale):
    n = rng.random((h // scale + 3, w // scale + 3)).astype(np.float32)
    im = Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale / 2))
    return np.asarray(im, np.float32) / 255

PALETTES = {  # key: (top, bottom, tints[(color, strength, scale)])
    "blue":   ("#050914", "#0B1530", [("#3987FF", .45, 260), ("#8957FF", .38, 340), ("#35D5E8", .2, 420)]),
    "purple": ("#060813", "#150F33", [("#8957FF", .5, 300), ("#3987FF", .3, 380), ("#F04FB5", .12, 460)]),
    "teal":   ("#050C16", "#081C2B", [("#35D5E8", .38, 300), ("#3987FF", .34, 360), ("#35D39A", .1, 480)]),
    "green":  ("#04100E", "#07251C", [("#35D39A", .42, 300), ("#35D5E8", .25, 380), ("#3987FF", .12, 460)]),
    "amber":  ("#120C05", "#2A1608", [("#FFBF69", .35, 300), ("#FF6B3D", .3, 380), ("#8957FF", .1, 460)]),
    "red":    ("#13060A", "#2A0C14", [("#FF647C", .35, 300), ("#8957FF", .25, 380), ("#FFBF69", .1, 460)]),
    "gold":   ("#0F0C05", "#241B08", [("#FFD84A", .3, 300), ("#FF8A1F", .25, 380), ("#8957FF", .1, 460)]),
    "slate":  ("#070B14", "#101828", [("#3987FF", .2, 300), ("#35D5E8", .12, 380), ("#8957FF", .1, 460)]),
}

def nebula(w, h, seed, key="blue", stars=1800, vignette=.38):
    top, bottom, tints = PALETTES[key]; rng = np.random.default_rng(seed)
    arr = np.asarray(gradient(w, h, [top, bottom]), np.float32).copy()
    for color, strength, scale in tints:
        a = (noise_field(rng, w, h, max(40, int(scale * w / 1920))) ** 3.0 * strength)[..., None]
        arr += np.array(hexrgb(color), np.float32) * a
    if stars:
        layer = Image.new("L", (w, h), 0); d = ImageDraw.Draw(layer); k = w * h / (1920 * 1080)
        for _ in range(int(stars * k)): d.point((int(rng.integers(0, w)), int(rng.integers(0, h))), fill=int(rng.integers(70, 220)))
        for _ in range(int(stars * k / 18)):
            x, y = int(rng.integers(0, w)), int(rng.integers(0, h)); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=255)
        arr += (np.asarray(layer.filter(ImageFilter.GaussianBlur(.6)), np.float32)[..., None] / 255) * np.array([200, 225, 255], np.float32) * .9
    yy, xx = np.mgrid[0:h, 0:w]; r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    arr *= (1 - vignette * np.clip(r - .45, 0, 1) ** 1.4)[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

def halo(im, cx, cy, r, color, a=0.5):
    """Soft radial glow composited onto `im` (RGBA, modified in place)."""
    w, h = im.size; x0, y0 = int(max(0, cx - r)), int(max(0, cy - r)); x1, y1 = int(min(w, cx + r)), int(min(h, cy + r))
    if x1 <= x0 or y1 <= y0: return
    yy, xx = np.mgrid[y0:y1, x0:x1]; d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    alpha = np.clip(1 - d, 0, 1) ** 2 * a * 255
    patch = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); patch[..., :3] = hexrgb(color); patch[..., 3] = alpha.astype(np.uint8)
    im.alpha_composite(Image.fromarray(patch, "RGBA"), (x0, y0))

def comp(dst, src, x, y):
    """alpha_composite with clipping (works when src is partly outside dst)."""
    x, y = int(x), int(y); w, h = dst.size
    sx0, sy0 = max(0, -x), max(0, -y); sx1, sy1 = min(src.width, w - x), min(src.height, h - y)
    if sx1 <= sx0 or sy1 <= sy0: return
    dst.alpha_composite(src.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))

# ───────── geometry helpers ─────────
def rad(a): return math.radians(a)
def arc_pts(cx, cy, r, a0, a1):
    n = max(8, int(abs(a1 - a0) / 6)); return [(cx + r * math.cos(rad(a0 + (a1 - a0) * i / n)), cy + r * math.sin(rad(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
def ell_pts(cx, cy, rx, ry, rot=0, n=72):
    out_ = []
    for i in range(n + 1):
        t = rad(360 * i / n); x, y = rx * math.cos(t), ry * math.sin(t); a = rad(rot)
        out_.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return out_
def rrect_pts(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return (arc_pts(x + w - r, y + r, r, -90, 0) + arc_pts(x + w - r, y + h - r, r, 0, 90) + arc_pts(x + r, y + h - r, r, 90, 180) + arc_pts(x + r, y + r, r, 180, 270))
def star_pts(cx, cy, ro, ri, n=5, rot=-90):
    return [(cx + (ro if i % 2 == 0 else ri) * math.cos(rad(rot + 180 * i / n)), cy + (ro if i % 2 == 0 else ri) * math.sin(rad(rot + 180 * i / n))) for i in range(2 * n)]

# ───────── Art layer (supersampled, transparent) ─────────
class Art:
    def __init__(self, w, h, ss=2):
        self.w, self.h, self.ss = w, h, ss
        self.im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.im)
    def _p(self, pts): return [(x * self.ss, y * self.ss) for x, y in pts]
    def line(self, pts, color, width=2, closed=False):
        pts = list(pts) + ([pts[0]] if closed else []); q = self._p(pts); wpx = max(1, int(width * self.ss))
        self.d.line(q, fill=color, width=wpx, joint="curve"); r = wpx / 2
        for x, y in (q[0], q[-1]): self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    def poly(self, pts, fill): self.d.polygon(self._p(pts), fill=fill)
    def circle(self, cx, cy, r, fill=None, outline=None, width=1):
        s = self.ss; self.d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=fill, outline=outline, width=max(1, int(width * s)) if outline else 0)
    def ring(self, cx, cy, rx, ry, color, width=2, rot=0): self.line(ell_pts(cx, cy, rx, ry, rot), color, width)
    def glyph(self, name, cx, cy, size, color, width=2.0):
        width = GLYPH_W.get(name, width); s = size / 24.0
        for kind, *a in glyph_prims(name):
            if kind == "line": pts, closed = a; self.line([(cx + (x - 12) * s, cy + (y - 12) * s) for x, y in pts], color, width * s, closed)
            else: x, y, r = a; self.circle(cx + (x - 12) * s, cy + (y - 12) * s, r * s, fill=color)
    def result(self, glow=0, strength=0.9):
        base = self.im.resize((self.w, self.h), Image.LANCZOS)
        if not glow: return base
        g = base.filter(ImageFilter.GaussianBlur(glow)); r, gr, b, a = g.split(); a = a.point(lambda v: int(min(255, v * strength * 1.6)))
        return Image.alpha_composite(Image.merge("RGBA", (r, gr, b, a)), base)

def grad_poly(size, pts, top, bottom, mid=None, ss=3, alpha=255, mode="v"):
    """Anti-aliased polygon filled with a gradient, returned as a transparent RGBA layer."""
    w, h = size; m = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(m).polygon([(x * ss, y * ss) for x, y in pts], fill=alpha); m = m.resize((w, h), Image.LANCZOS)
    g = gradient(w, h, [top] + ([mid] if mid else []) + [bottom], mode).convert("RGBA"); g.putalpha(m); return g

# ───────── glyph engine (24x24 line icons, Lucide-style) ─────────
def _l(x1, y1, x2, y2): return ("l", x1, y1, x2, y2)
def _p(*pts): return ("p", list(pts))
def _g(*pts): return ("g", list(pts))
def _c(cx, cy, r): return ("c", cx, cy, r)
def _d(cx, cy, r): return ("d", cx, cy, r)
def _r(x, y, w, h, r=2): return ("r", x, y, w, h, r)
def _a(cx, cy, r, a0, a1): return ("a", cx, cy, r, a0, a1)
def _e(cx, cy, rx, ry, rot=0): return ("e", cx, cy, rx, ry, rot)

def _sine(x0, x1, cy, amp, cycles, phase=0, n=40):
    return [(x0 + (x1 - x0) * i / n, cy + amp * math.sin(rad(360 * cycles * i / n + phase))) for i in range(n + 1)]

GLYPHS = {
    "home": [_p((3, 11), (12, 3), (21, 11)), _p((5, 10), (5, 21), (19, 21), (19, 10)), _p((10, 21), (10, 14), (14, 14), (14, 21))],
    "learn": [_p((12, 6), (8, 4.5), (3, 4.5), (3, 18.5), (8, 18.5), (12, 20)), _p((12, 6), (16, 4.5), (21, 4.5), (21, 18.5), (16, 18.5), (12, 20)), _l(12, 6, 12, 20)],
    "lab": [_l(8, 3, 16, 3), _p((10, 3), (10, 9), (4, 19), (5, 21), (19, 21), (20, 19), (14, 9), (14, 3)), _l(7, 15, 17, 15)],
    "games": [_r(2, 7, 20, 12, 5), _l(7, 10, 7, 14), _l(5, 12, 9, 12), _d(15.5, 11, 1), _d(18, 13.5, 1)],
    "trophy": [_g((7, 4), (17, 4), (17, 10), (14.5, 13), (9.5, 13), (7, 10)), _p((7, 5), (4, 5), (4, 8), (7, 10)), _p((17, 5), (20, 5), (20, 8), (17, 10)), _l(12, 13, 12, 17), _p((9, 21), (9, 17), (15, 17), (15, 21)), _l(7, 21, 17, 21)],
    "bot": [_r(4, 8, 16, 11, 3), _l(12, 4.5, 12, 8), _d(12, 3.5, 1.3), _d(9, 12.5, 1.3), _d(15, 12.5, 1.3), _a(12, 14, 3, 20, 160), _l(2, 12, 4, 12), _l(20, 12, 22, 12)],
    "settings": [_c(12, 12, 3)] + [_l(12 + 6.5 * math.cos(rad(k * 45)), 12 + 6.5 * math.sin(rad(k * 45)), 12 + 9.5 * math.cos(rad(k * 45)), 12 + 9.5 * math.sin(rad(k * 45))) for k in range(8)] + [_c(12, 12, 6.5)],
    "user": [_c(12, 8, 4), _a(12, 21, 8, 180, 360)],
    "bell": [_a(12, 10, 6, 180, 360), _l(6, 10, 6, 16), _l(18, 10, 18, 16), _l(4, 17, 20, 17), _a(12, 19.5, 2, 0, 180)],
    "search": [_c(10.5, 10.5, 6.5), _l(15.5, 15.5, 21, 21)],
    "video": [_r(3, 5, 18, 14, 3), _g((10, 9), (10, 15), (15.5, 12))],
    "file": [_g((6, 3), (14, 3), (19, 8), (19, 21), (6, 21)), _p((14, 3), (14, 8), (19, 8)), _l(9, 13, 16, 13), _l(9, 17, 16, 17)],
    "note": [_r(4, 3, 16, 18, 2), _l(8, 8, 16, 8), _l(8, 12, 16, 12), _l(8, 16, 13, 16)],
    "quiz": [_r(5, 4, 14, 17, 2), _r(9, 2, 6, 4, 1), _p((9, 13), (11.5, 15.5), (15.5, 10.5))],
    "points": [("g", star_pts(12, 12.5, 9, 3.9))],
    "level": [_p((6, 11), (12, 5), (18, 11)), _p((6, 18), (12, 12), (18, 18))],
    "award": [_c(12, 9, 5.5), _p((9, 14), (8, 21), (12, 19), (16, 21), (15, 14))],
    "calendar": [_r(3, 5, 18, 16, 2), _l(3, 10, 21, 10), _l(8, 3, 8, 7), _l(16, 3, 16, 7)],
    "download": [_l(12, 4, 12, 15), _p((7, 11), (12, 16), (17, 11)), _l(4, 19, 20, 19)],
    "volume": [_g((4, 9), (8, 9), (13, 5), (13, 19), (8, 15), (4, 15)), _a(14, 12, 4, -50, 50), _a(14, 12, 8, -45, 45)],
    "mic": [_r(9, 3, 6, 11, 3), _a(12, 11, 7, 0, 180), _l(12, 18, 12, 21), _l(9, 21, 15, 21)],
    "camera": [_g((3, 8), (7, 8), (9, 5), (15, 5), (17, 8), (21, 8), (21, 19), (3, 19)), _c(12, 13, 3.5)],
    "back": [_l(4, 12, 20, 12), _p((14, 6), (20, 12), (14, 18))],
    "next": [_l(4, 12, 20, 12), _p((10, 6), (4, 12), (10, 18))],
    "close": [_l(6, 6, 18, 18), _l(18, 6, 6, 18)],
    "help": [_c(12, 12, 9.5), _a(12, 10, 3, 180, 400), _l(12, 13, 12, 14), _d(12, 17, 1)],
    "privacy": [_g((12, 3), (19, 6), (19, 12), (12, 21), (5, 12), (5, 6)), _p((9, 12), (11, 14), (15, 10))],
    # extra glyphs used by illustrations / badges
    "atom": [_e(12, 12, 10, 4, 0), _e(12, 12, 10, 4, 60), _e(12, 12, 10, 4, 120), _d(12, 12, 1.6)],
    "dna": [("p", [(12 + 6 * math.sin(rad(540 * k / 24)), 3 + 18 * k / 24) for k in range(25)]), ("p", [(12 - 6 * math.sin(rad(540 * k / 24)), 3 + 18 * k / 24) for k in range(25)])] + [_l(12 + 6 * math.sin(rad(540 * k / 24)), 3 + 18 * k / 24, 12 - 6 * math.sin(rad(540 * k / 24)), 3 + 18 * k / 24) for k in (4, 12, 20)],
    "check": [_c(12, 12, 9.5), _p((8, 12.5), (11, 15.5), (16.5, 9))],
    "flame": [_g((12, 3), (16, 8), (18, 13), (16, 19), (12, 21), (8, 19), (6, 13), (8.5, 10), (10, 12), (11, 8))],
    "repeat": [_a(12, 12, 8, 200, 340), _p((17, 3.5), (19.5, 6.5), (16, 8.5)), _a(12, 12, 8, 20, 160), _p((7, 20.5), (4.5, 17.5), (8, 15.5))],
    "target": [_c(12, 12, 9), _c(12, 12, 5), _d(12, 12, 1.6)],
    "bars": [_r(4, 12, 4, 8, 1), _r(10, 6, 4, 14, 1), _r(16, 9, 4, 11, 1), _l(3, 21, 21, 21)],
    "chart": [_p((3, 17), (8, 11), (12, 14), (21, 5)), _p((16, 5), (21, 5), (21, 10)), _l(3, 21, 21, 21)],
    "clock": [_c(12, 12, 9.5), _p((12, 6.5), (12, 12), (16, 14))],
    "box": [_g((12, 3), (20, 7.5), (20, 16.5), (12, 21), (4, 16.5), (4, 7.5)), _p((4, 7.5), (12, 12), (20, 7.5)), _l(12, 12, 12, 21)],
    "crown": [_g((3, 18), (3, 8), (8, 12), (12, 5), (16, 12), (21, 8), (21, 18)), _l(3, 21, 21, 21)],
    "spark": [("g", star_pts(12, 12, 10, 2.6, 4, -90))],
    "wifioff": [_a(12, 19, 14, 235, 305), _a(12, 19, 9, 235, 305), _a(12, 19, 4, 235, 305), _d(12, 19, 1.2), _l(3, 3, 21, 21)],
    "warning": [_g((12, 3), (22, 20), (2, 20)), _l(12, 9, 12, 14), _d(12, 17, 1)],
    "bulb": [_a(12, 10, 6, 150, 390), _l(9.5, 16.5, 14.5, 16.5), _l(10, 19, 14, 19)],
    "wave": [("p", _sine(2, 22, 12, 5, 2))],
    "download2": [_l(12, 3, 12, 14), _p((7, 10), (12, 15), (17, 10)), _r(4, 17, 16, 4, 1)],
    "puzzle": [_g((4, 4), (11, 4), (11, 6), (13, 6), (13, 4), (20, 4), (20, 11), (18, 11), (18, 13), (20, 13), (20, 20), (4, 20))],
}
GLYPH_W = {"dna": 1.3, "atom": 1.7, "puzzle": 1.9, "flame": 1.9}
ICON_NAMES = ["home", "learn", "lab", "games", "trophy", "bot", "settings", "user", "bell", "search", "video", "file", "note", "quiz", "points", "level",
              "award", "calendar", "download", "volume", "mic", "camera", "back", "next", "close", "help", "privacy", "level"]

def glyph_prims(name):
    """Expands a glyph into ('line', pts, closed) and ('dot', x, y, r) primitives."""
    res = []
    for prim in GLYPHS[name]:
        k = prim[0]
        if k == "l": res.append(("line", [(prim[1], prim[2]), (prim[3], prim[4])], False))
        elif k == "p": res.append(("line", prim[1], False))
        elif k == "g": res.append(("line", prim[1], True))
        elif k == "c": res.append(("line", ell_pts(prim[1], prim[2], prim[3], prim[3], 0, 48)[:-1], True))
        elif k == "d": res.append(("dot", prim[1], prim[2], prim[3]))
        elif k == "r": res.append(("line", rrect_pts(*prim[1:6]), True))
        elif k == "a": res.append(("line", arc_pts(prim[1], prim[2], prim[3], prim[4], prim[5]), False))
        elif k == "e": res.append(("line", ell_pts(prim[1], prim[2], prim[3], prim[4], prim[5], 60)[:-1], True))
    return res

def icon_svg(name):
    parts = []
    for kind, *a in glyph_prims(name):
        if kind == "line":
            pts, closed = a; d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + (" Z" if closed else ""); parts.append(f'<path d="{d}"/>')
        else: x, y, r = a; parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="currentColor" stroke="none"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="%s">%s</svg>\n' % (name, "".join(parts)))
