#!/usr/bin/env python3
"""Reproducible procedural asset generator (PIL + numpy only).
Run from anywhere:  python3 PHYSICS_ACADEMY_ASSETS/tools/generate_assets.py
Produces: logo (SVG+PNG), app icon, web icon, 3 backgrounds, 15 level badges (SVG+PNG), concept art WebP."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def out(*p):
    path = os.path.join(ROOT, *p); os.makedirs(os.path.dirname(path), exist_ok=True); return path
def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ───────── logo / icons ─────────
G1, G2, G3 = "#35D5E8", "#3987FF", "#8957FF"
ORBITS = [0, 60, 120]
def diag_gradient(size):
    x = np.linspace(0, 1, size)[None, :]; y = np.linspace(0, 1, size)[:, None]; t = (x + y) / 2
    c1, c2, c3 = map(np.array, map(hexrgb, (G1, G2, G3)))
    t3 = t[..., None]
    return np.where(t3 < .5, c1 + (c2 - c1) * (t3 * 2), c2 + (c3 - c2) * ((t3 - .5) * 2)).astype(np.uint8)

def mark_layer(size):
    """Orbit mark on a transparent RGBA square of `size` px (drawn at 2x then downsampled)."""
    ss = 2; S = size * ss; k = S / 512
    mask = Image.new("L", (S, S), 0); d = ImageDraw.Draw(mask)
    for ang in ORBITS:
        pts = []
        for i in range(361):
            t = math.radians(i); x, y = 170 * math.cos(t), 62 * math.sin(t)
            a = math.radians(ang); pts.append(((256 + x * math.cos(a) - y * math.sin(a)) * k, (256 + x * math.sin(a) + y * math.cos(a)) * k))
        d.line(pts, fill=255, width=int(14 * k), joint="curve")
    r = 26 * k; d.ellipse([256 * k - r, 256 * k - r, 256 * k + r, 256 * k + r], fill=255)
    glow = mask.filter(ImageFilter.GaussianBlur(10 * k)).point(lambda v: int(v * .55))
    grad = Image.fromarray(diag_gradient(S), "RGB")
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    layer.paste(Image.merge("RGBA", (*grad.split(), glow)), (0, 0))
    solid = Image.new("RGBA", (S, S), (0, 0, 0, 0)); solid.paste(grad, (0, 0), mask)
    layer = Image.alpha_composite(layer, solid)
    return layer.resize((size, size), Image.LANCZOS)

def mark_svg_body(scale=1.0, tx=0, ty=0):
    ell = "".join(f'<ellipse cx="256" cy="256" rx="170" ry="62" transform="rotate({a} 256 256)" fill="none" stroke="url(#g)" stroke-width="14"/>' for a in ORBITS)
    return (f'<g transform="translate({tx} {ty}) scale({scale})">{ell}<circle cx="256" cy="256" r="26" fill="url(#g)"/></g>')
GRAD_DEF = f'<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="60" y1="60" x2="452" y2="452"><stop offset="0" stop-color="{G1}"/><stop offset=".5" stop-color="{G2}"/><stop offset="1" stop-color="{G3}"/></linearGradient>'

def write(path, text): open(out(path), "w", encoding="utf-8").write(text)

def make_logo():
    # mark only (used in app headers) — transparent
    write("01_BRANDING/logo/logo-mark.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="Physics Academy"><defs>{GRAD_DEF}</defs>{mark_svg_body()}</svg>')
    # full logo (transparent) = mark + wordmark; SVG keeps live text (font fallback), PNG is rendered
    write("01_BRANDING/logo/physics_academy_logo_transparent.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="Physics Academy"><defs>{GRAD_DEF}</defs>'
          f'{mark_svg_body(0.72, 71.7, 0)}<text x="256" y="430" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="700" font-size="40" fill="#EAF2FF" letter-spacing="3">PHYSICS ACADEMY</text>'
          f'<text x="256" y="466" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="700" font-size="20" fill="#72C7FF" letter-spacing="8">QUANTUM</text></svg>')
    S = 1024; img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    m = mark_layer(int(S * .72)); img.alpha_composite(m, ((S - m.width) // 2, int(S * -0.0)))
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype(FONT, 80); f2 = ImageFont.truetype(FONT, 40)
    d.text((S / 2, 860), "PHYSICS ACADEMY", font=f1, fill="#EAF2FF", anchor="mm")
    d.text((S / 2, 932), "Q U A N T U M", font=f2, fill="#72C7FF", anchor="mm")
    img.save(out("01_BRANDING/logo/physics_academy_logo.png"))
    # app icon: opaque, full-bleed, mark inside the 66% adaptive-icon safe zone
    bg = np.zeros((S, S, 3), np.float32); x = np.linspace(0, 1, S)[None, :]; y = np.linspace(0, 1, S)[:, None]; t = ((x + y) / 2)[..., None]
    bg[:] = np.array(hexrgb("#0A1226")) * (1 - t) + np.array(hexrgb("#1B2F6B")) * t
    icon = Image.fromarray(bg.astype(np.uint8), "RGB").convert("RGBA")
    m = mark_layer(int(S * .62)); icon.alpha_composite(m, ((S - m.width) // 2, (S - m.height) // 2))
    icon.convert("RGB").save(out("01_BRANDING/app_icon/app_icon.png"))
    write("01_BRANDING/app_icon/app_icon.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs>{GRAD_DEF}<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A1226"/><stop offset="1" stop-color="#1B2F6B"/></linearGradient></defs><rect width="512" height="512" rx="112" fill="url(#bg)"/>{mark_svg_body(0.62, 97, 97)}</svg>')

# ───────── level badges ─────────
def poly(n, rot=0): return [(math.cos(math.radians(rot + 360 * i / n - 90)), math.sin(math.radians(rot + 360 * i / n - 90))) for i in range(n)]
def star(n, inner):
    pts = []
    for i in range(2 * n):
        r = 1 if i % 2 == 0 else inner; a = math.radians(180 * i / n - 90); pts.append((r * math.cos(a), r * math.sin(a)))
    return pts
def gear(n, depth):
    pts = []; step = 2 * math.pi / n
    for i in range(n):
        a = i * step - math.pi / 2
        for off, r in ((-.30, 1 - depth), (-.16, 1), (.16, 1), (.30, 1 - depth)):
            pts.append((r * math.cos(a + off * step * 1.6), r * math.sin(a + off * step * 1.6)))
    return pts
def shield():
    pts = [(-.82, -.78), (0, -.9), (.82, -.78)]
    for i in range(1, 13):  # right side curving to the tip
        t = i / 12; pts.append((.82 * (1 - t ** 2.2) , -.78 + 1.73 * t ** 0.9 if t > .35 else -.78 + 0.85 * t / .35 * .35 + t * 0))
    pts = [(-.82, -.80), (0, -.92), (.82, -.80), (.82, -.05)]
    for i in range(1, 9):
        t = i / 9; pts.append((.82 * math.cos(t * math.pi / 2) ** 1.1, -.05 + 1.0 * math.sin(t * math.pi / 2) ** 1.3))
    pts.append((0, .97))
    right = pts[3:-1]; left = [(-x, y) for x, y in reversed(right)]
    return [(-.82, -.80), (0, -.92), (.82, -.80)] + right + [(0, .97)] + left
SHAPES = [poly(96), gear(16, .05), poly(6), poly(4), poly(8, 22.5), star(5, .55), shield(), star(6, .6), poly(10), star(8, .68), gear(10, .12), star(7, .62), star(9, .72), gear(12, .14), star(12, .80)]
PAL = [("#E6EAF0", "#AEB7C4", "#6B7686"), ("#FFE58A", "#F2B632", "#9A6A0C"), ("#F4F6FA", "#C9D3E3", "#7C8BA5"), ("#D9F7FF", "#6FD8F5", "#2A7FA8"),
       ("#B8FFF0", "#2FD6B8", "#0D7566"), ("#FFF0B0", "#FFB830", "#B35A00"), ("#FFD0B0", "#FF6B3D", "#9E2A10"), ("#FFC6EA", "#F04FB5", "#8A1666"),
       ("#E3D4FF", "#9B6BFF", "#4C23A8"), ("#C9D6FF", "#4E73FF", "#1B2F9E"), ("#D4F8C4", "#5CCB4E", "#1E7A22"), ("#FFC2CB", "#E5384F", "#8A0F24"),
       ("#F3C9FF", "#C04DFF", "#6A12A8"), ("#FFE0D2", "#E8A08A", "#9B5440"), ("#FFFBD6", "#FFD84A", "#FF8A1F")]
SLUGS = ["silver", "gold", "platinum", "diamond", "elite", "star", "hero", "top", "expert", "innovator", "sage", "scholar", "genius", "master", "legend"]
def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in hexrgb(c))
def vgrad(S, stops):
    y = np.linspace(0, 1, S)[:, None, None]; arr = np.zeros((S, S, 3), np.float32); a, b, c = [np.array(s, np.float32) for s in stops]
    arr[:] = np.where(y < .5, a + (b - a) * (y * 2), b + (c - b) * ((y - .5) * 2)); return Image.fromarray(arr.astype(np.uint8), "RGB")

def badge(i):
    shape, (lt, md, dk) = SHAPES[i], PAL[i]; lvl = i + 1; ss = 2; S = 512 * ss; cx = cy = S / 2; R = 225 * ss
    def pts(scale): return [(cx + x * R * scale, cy + y * R * scale) for x, y in shape]
    def mask(scale, stroke=0):
        m = Image.new("L", (S, S), 0); d = ImageDraw.Draw(m)
        if stroke: d.line(pts(scale) + [pts(scale)[0]], fill=255, width=stroke, joint="curve")
        else: d.polygon(pts(scale), fill=255)
        return m
    canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    if lvl == 15:
        g = mask(1.05).filter(ImageFilter.GaussianBlur(26 * ss)); glow = Image.new("RGBA", (S, S), hexrgb(md) + (0,)); glow.putalpha(g.point(lambda v: int(v * .9))); canvas.alpha_composite(glow)
    shadow = mask(1.0).filter(ImageFilter.GaussianBlur(8 * ss)).point(lambda v: int(v * .45)); sh = Image.new("RGBA", (S, S), (0, 0, 0, 0)); sh.putalpha(shadow)
    canvas.alpha_composite(sh, (0, 8 * ss))
    rim = Image.new("RGBA", (S, S), (0, 0, 0, 0)); rim.paste(vgrad(S, [hexrgb(lt), hexrgb(md), hexrgb(dk)]), (0, 0), mask(1.0)); canvas.alpha_composite(rim)
    face = Image.new("RGBA", (S, S), (0, 0, 0, 0)); face.paste(vgrad(S, [shade(dk, .75), shade(md, .8), shade(md, 1.0)]), (0, 0), mask(.80)); canvas.alpha_composite(face)
    hl = Image.new("RGBA", (S, S), (0, 0, 0, 0)); hl.paste(Image.new("RGB", (S, S), hexrgb(lt)), (0, 0), mask(.80, 3 * ss).point(lambda v: int(v * .7))); canvas.alpha_composite(hl)
    d = ImageDraw.Draw(canvas); f = ImageFont.truetype(FONT, 210 * ss if lvl < 10 else 170 * ss)
    d.text((cx, cy + 6 * ss), str(lvl), font=f, fill="#FFFFFF", anchor="mm", stroke_width=5 * ss, stroke_fill=shade(dk, .45))
    canvas.resize((512, 512), Image.LANCZOS).save(out("06_REWARDS/levels", f"level_{lvl:02d}_{SLUGS[i]}.png"))
    # SVG twin
    def sp(scale): return " ".join(f"{256 + x * 225 * scale:.1f},{256 + y * 225 * scale:.1f}" for x, y in shape)
    glow_def = '<filter id="gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>'
    glow_el = f'<polygon points="{sp(1.05)}" fill="{md}" filter="url(#gl)" opacity=".85"/>' if lvl == 15 else ""
    write(f"06_REWARDS/levels/level_{lvl:02d}_{SLUGS[i]}.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="Level {lvl}"><defs>{glow_def}'
          f'<linearGradient id="r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{lt}"/><stop offset=".5" stop-color="{md}"/><stop offset="1" stop-color="{dk}"/></linearGradient>'
          f'<linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgb{shade(dk, .75)}"/><stop offset=".5" stop-color="rgb{shade(md, .8)}"/><stop offset="1" stop-color="{md}"/></linearGradient></defs>'
          f'{glow_el}<polygon points="{sp(1.0)}" fill="url(#r)"/><polygon points="{sp(.80)}" fill="url(#f)" stroke="{lt}" stroke-opacity=".7" stroke-width="3"/>'
          f'<text x="256" y="{256 + 74 if lvl < 10 else 256 + 60}" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="800" font-size="{210 if lvl < 10 else 170}" fill="#fff" stroke="rgb{shade(dk, .45)}" stroke-width="10" paint-order="stroke">{lvl}</text></svg>')

# ───────── backgrounds ─────────
def noise_field(rng, w, h, scale):
    n = rng.random((h // scale + 3, w // scale + 3)).astype(np.float32)
    im = Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale / 2))
    return np.asarray(im, np.float32) / 255
def background(name, seed, top, bottom, tints, extra=None, w=1920, h=1080):
    rng = np.random.default_rng(seed); t = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(hexrgb(top), np.float32) * (1 - t) + np.array(hexrgb(bottom), np.float32) * t; arr = np.broadcast_to(arr, (h, w, 3)).copy()
    for color, strength, scale in tints:
        a = (noise_field(rng, w, h, scale) ** 3.0 * strength)[..., None]; arr += np.array(hexrgb(color), np.float32) * a
    layer = Image.new("L", (w, h), 0); d = ImageDraw.Draw(layer)
    for _ in range(2600):
        x, y = int(rng.integers(0, w)), int(rng.integers(0, h)); v = int(rng.integers(70, 220)); d.point((x, y), fill=v)
    for _ in range(140):
        x, y = int(rng.integers(0, w)), int(rng.integers(0, h)); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=255)
    stars = np.asarray(layer.filter(ImageFilter.GaussianBlur(.6)), np.float32)[..., None] / 255
    arr += stars * np.array([200, 225, 255], np.float32) * .9
    if extra: arr = extra(arr, rng, w, h)
    yy, xx = np.mgrid[0:h, 0:w]; r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2); arr *= (1 - .38 * np.clip(r - .45, 0, 1) ** 1.4)[..., None]
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(out("01_BRANDING/backgrounds", name), quality=80, method=6)
def rings(arr, rng, w, h):
    lay = Image.new("L", (w, h), 0); d = ImageDraw.Draw(lay)
    for rx, ry in ((520, 190), (420, 150), (320, 112)):
        for ang in (0, 60, 120):
            pts = [(w * .78 + rx * math.cos(math.radians(i)) * math.cos(math.radians(ang)) - ry * math.sin(math.radians(i)) * math.sin(math.radians(ang)),
                    h * .45 + rx * math.cos(math.radians(i)) * math.sin(math.radians(ang)) + ry * math.sin(math.radians(i)) * math.cos(math.radians(ang))) for i in range(361)]
            d.line(pts, fill=70, width=2)
    return arr + np.asarray(lay.filter(ImageFilter.GaussianBlur(1.2)), np.float32)[..., None] / 255 * np.array([90, 150, 255], np.float32)
def floor_grid(arr, rng, w, h):
    lay = Image.new("L", (w, h), 0); d = ImageDraw.Draw(lay); horizon = int(h * .66); vx = w / 2
    y = horizon; gap = 6
    while y < h: d.line([(0, y), (w, y)], fill=int(25 + 60 * (y - horizon) / (h - horizon))); gap *= 1.22; y += gap
    for i in range(-30, 31): d.line([(vx, horizon), (vx + i * 170, h)], fill=60)
    return arr + np.asarray(lay.filter(ImageFilter.GaussianBlur(.8)), np.float32)[..., None] / 255 * np.array([53, 213, 232], np.float32) * .7
def make_backgrounds():
    background("main_background.webp", 11, "#050914", "#0B1530", [("#3987FF", 0.45, 260), ("#8957FF", 0.38, 340), ("#35D5E8", 0.2, 420)])
    background("auth_background.webp", 23, "#060813", "#150F33", [("#8957FF", 0.5, 300), ("#3987FF", 0.3, 380), ("#F04FB5", 0.12, 460)], rings)
    background("learning_room.webp", 37, "#050C16", "#081C2B", [("#35D5E8", 0.38, 300), ("#3987FF", 0.34, 360), ("#35D39A", 0.1, 480)], floor_grid)

if __name__ == "__main__":
    make_logo(); make_backgrounds()
    for i in range(15): badge(i)
    src = out("08_UI_ILLUSTRATIONS/quantum-dashboard-concept.png")
    if os.path.exists(src): Image.open(src).convert("RGB").save(out("08_UI_ILLUSTRATIONS/quantum-dashboard-concept.webp"), quality=82, method=6)
    print("assets generated")
