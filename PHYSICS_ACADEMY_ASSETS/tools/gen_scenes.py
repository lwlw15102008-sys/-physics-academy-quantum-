"""Scene-style assets (opaque WebP): subjects, labs, games, competitions, UI states, analytics, subscriptions, website."""
import random
from toolkit import *

def S(base, f): return max(2, base * f)

# ───────── subject motifs ─────────
def paint_physics(w, h, s=1.0):
    art = Art(w, h); base = min(w, h); cx, cy = w * .5, h * .5; lw = S(base, .006)
    for ang, col in ((0, "#6FB4FF"), (60, "#9B7BFF"), (120, "#35D5E8")):
        art.ring(cx, cy, base * .46 * s, base * .16 * s, C(col, 210), lw, rot=ang)
        t = rad(ang * 2.3 + 40); x, y = base * .46 * s * math.cos(t), base * .16 * s * math.sin(t); a = rad(ang)
        art.circle(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a), base * .022, fill=C("#FFFFFF"))
    for i, (dx, dy, col) in enumerate(((0, 0, "#FFD84A"), (-.025, .02, "#FF6B3D"), (.028, .018, "#35D5E8"), (.0, -.03, "#FF6B3D"))):
        art.circle(cx + dx * base, cy + dy * base, base * (.05 if i == 0 else .035), fill=C(col))
    return art.result(glow=base * .012)

def paint_chemistry(w, h, s=1.0):
    art = Art(w, h); base = min(w, h); R = base * .13 * s; lw = S(base, .007); cols = ["#35D5E8", "#FFFFFF", "#FF647C", "#FFD84A"]
    hexes = [(w * .5, h * .46), (w * .5 + R * 1.73, h * .46 - R * 1.5 * .0 + R * 1.5), (w * .5 - R * 1.73, h * .46 + R * 1.5), (w * .5 + R * 1.73, h * .46 - R * 1.5), (w * .5 - R * 1.73, h * .46 - R * 1.5)]
    for (cx, cy) in hexes:
        pts = [(cx + R * math.cos(rad(60 * k - 30)), cy + R * math.sin(rad(60 * k - 30))) for k in range(6)]
        art.line(pts, C("#8FE8F2", 170), lw, closed=True)
        for k, (x, y) in enumerate(pts): art.circle(x, y, base * .03, fill=C(cols[k % 4]))
    rnd = random.Random(7)
    for _ in range(26):
        x, y, r = rnd.uniform(0, w), rnd.uniform(h * .55, h), rnd.uniform(base * .008, base * .035); art.circle(x, y, r, outline=C("#BFF6FF", 120), width=lw * .6)
    art.glyph("lab", w * .84, h * .3, base * .3, C("#9BF0FA", 150), width=2.4)
    return art.result(glow=base * .01)

def paint_biology(w, h, s=1.0):
    art = Art(w, h); base = min(w, h); lw = S(base, .008); rnd = random.Random(11)
    for _ in range(9):
        x, y, r = rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(base * .05, base * .13)
        art.circle(x, y, r, fill=C("#35D39A", 28), outline=C("#7DF0C4", 110), width=lw * .6); art.circle(x + r * .2, y - r * .1, r * .32, fill=C("#B08AFF", 90))
    x0, y0, x1, y1 = w * .12, h * .86, w * .88, h * .14; n = 60; A = base * .1 * s
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    sa, sb = [], []
    for i in range(n + 1):
        t = i / n; ph = rad(t * 720); px, py = x0 + dx * t, y0 + dy * t
        sa.append((px + nx * A * math.sin(ph), py + ny * A * math.sin(ph))); sb.append((px - nx * A * math.sin(ph), py - ny * A * math.sin(ph)))
        if i % 3 == 0: art.line([sa[-1], sb[-1]], C("#E3F9F0", 120), lw * .7)
    art.line(sa, C("#35D5E8", 235), lw * 1.5); art.line(sb, C("#F04FB5", 235), lw * 1.5)
    for i in range(0, n + 1, 3): art.circle(*sa[i], base * .012, fill=C("#FFFFFF")); art.circle(*sb[i], base * .012, fill=C("#FFFFFF"))
    return art.result(glow=base * .01)

def paint_math(w, h, s=1.0):
    art = Art(w, h); base = min(w, h); lw = S(base, .005); cx, cy = w * .5, h * .55
    for i in range(-10, 11):
        art.line([(cx + i * base * .08, 0), (cx + i * base * .08, h)], C("#9B7BFF", 40), lw * .6); art.line([(0, cy + i * base * .08), (w, cy + i * base * .08)], C("#9B7BFF", 40), lw * .6)
    art.line([(0, cy), (w, cy)], C("#C9B8FF", 160), lw); art.line([(cx, 0), (cx, h)], C("#C9B8FF", 160), lw)
    art.line([(cx + (i - 30) / 30 * w * .48, cy - base * .22 * math.sin(rad(i * 12))) for i in range(61)], C("#35D5E8", 235), lw * 1.6)
    art.line([(cx + (i - 30) / 30 * w * .3, cy + base * .5 - base * .55 * ((i - 30) / 30) ** 2 * 1.0 - base * .5 + base * .0) for i in range(61)], C("#FFD84A", 235), lw * 1.6)
    art.circle(cx, cy, base * .2, outline=C("#F04FB5", 220), width=lw * 1.4); art.line([(cx, cy), (cx + base * .2 * math.cos(rad(-38)), cy + base * .2 * math.sin(rad(-38)))], C("#FFFFFF", 230), lw)
    art.line([(w * .12, h * .82), (w * .3, h * .82), (w * .12, h * .6)], C("#35D39A", 220), lw * 1.3, closed=True)
    art.line([(w * .74, h * .22), (w * .9, h * .22), (w * .9, h * .38), (w * .74, h * .38)], C("#FF9F6B", 200), lw * 1.3, closed=True)
    return art.result(glow=base * .01)

def paint_geology(w, h, s=1.0):
    art = Art(w, h); base = min(w, h); lw = S(base, .004); rnd = random.Random(5)
    cols = ["#6B4430", "#9A6340", "#C4803F", "#8A4A2E", "#4A3028", "#2B1D1A"]
    for i, c in enumerate(cols):
        top = h * (.52 + i * .1); ph = rnd.uniform(0, 6)
        pts = [(x, top + base * .025 * math.sin(rad(x / w * 540 + ph * 57))) for x in range(0, w + 1, max(4, w // 80))]
        art.poly(pts + [(w, h), (0, h)], C(c, 245)); art.line(pts, C("#FFD9A8", 120), lw)
    mt = [(0, h * .6), (w * .14, h * .38), (w * .24, h * .5), (w * .38, h * .22), (w * .52, h * .48), (w * .66, h * .3), (w * .8, h * .5), (w * .92, h * .36), (w, h * .52), (w, h * .6)]
    art.poly(mt, C("#1B1220", 255)); art.line(mt[:-2], C("#FFB36B", 170), lw * 1.4)
    art.poly([(w * .36, h * .24), (w * .38, h * .22), (w * .4, h * .25)], C("#FFE3C4", 255))
    return art.result(glow=base * .006)

PAINTERS = {"physics": (paint_physics, "blue", 21), "chemistry": (paint_chemistry, "teal", 22), "biology": (paint_biology, "green", 23),
            "mathematics": (paint_math, "purple", 24), "geology": (paint_geology, "amber", 25)}
ACCENT = {"physics": "#3987FF", "chemistry": "#35D5E8", "biology": "#35D39A", "mathematics": "#A78BFA", "geology": "#FFBF69"}

def subject_scene(kind, w, h, dim=1.0, lab=False):
    fn, key, seed = PAINTERS[kind]; im = nebula(w, h, seed, key); halo(im, w * .5, h * .5, min(w, h) * .6, ACCENT[kind], .3 * dim)
    art = fn(w, h, 1.0)
    if dim < 1:
        r, g, b, a = art.split(); art = Image.merge("RGBA", (r, g, b, a.point(lambda v: int(v * dim))))
    im.alpha_composite(art)
    if lab:  # lab bench strip along the bottom
        bench = Art(w, h); y0 = h * .8
        bench.poly([(0, y0), (w, y0), (w, h), (0, h)], C("#0A1224", 235)); bench.line([(0, y0), (w, y0)], C("#35D5E8", 200), max(2, h * .004))
        im.alpha_composite(bench.result(glow=h * .01, strength=.5))
    return im

# ───────── glyph scenes ─────────
def glyph_scene(w, h, seed, key, accent, glyph, sats=(), progress=None, rays=False, confetti=False, disc=.3, cx=None, cy=None):
    im = nebula(w, h, seed, key); base = min(w, h); cx = w * .5 if cx is None else cx; cy = h * .5 if cy is None else cy
    halo(im, cx, cy, base * .75, accent, .38); art = Art(w, h); lw = S(base, .0045); r = base * disc
    if rays:
        for k in range(28): a = rad(k * 360 / 28); art.line([(cx + base * .34 * math.cos(a), cy + base * .34 * math.sin(a)), (cx + base * .75 * math.cos(a), cy + base * .75 * math.sin(a))], C(accent, 55), lw * 2.2)
    art.ring(cx, cy, base * .5, base * .17, C(accent, 120), lw, rot=20); art.ring(cx, cy, base * .5, base * .17, C(accent, 90), lw, rot=-38)
    art.circle(cx, cy, r, fill=C("#0A1226", 200), outline=C(accent, 235), width=lw * 1.6)
    if progress is not None:
        art.line(arc_pts(cx, cy, r * .86, 0, 360), C("#FFFFFF", 40), lw * 3); art.line(arc_pts(cx, cy, r * .86, -90, -90 + 360 * progress), C(accent, 255), lw * 3.4)
        art.glyph(glyph, cx, cy, r * .85, C("#FFFFFF"), 2.2)
    else: art.glyph(glyph, cx, cy, r * 1.15, C("#FFFFFF"), 2.2)
    for g, ang, dist, size in sats:
        a = rad(ang); x, y = cx + base * .5 * dist * math.cos(a) * 1.25, cy + base * .17 * dist * 2.2 * math.sin(a)
        art.circle(x, y, size * .75, fill=C("#0A1226", 210), outline=C(accent, 190), width=lw); art.glyph(g, x, y, size * 1.05, C(accent, 255), 2.2)
    if confetti:
        rnd = random.Random(seed)
        for _ in range(70):
            x, y = rnd.uniform(0, w), rnd.uniform(0, h); col = rnd.choice(["#FFD84A", "#35D5E8", "#F04FB5", "#A78BFA", "#35D39A"])
            t = rnd.uniform(0, 6.28); L = base * .018; art.line([(x, y), (x + L * math.cos(t), y + L * math.sin(t))], C(col, 230), lw * 1.6)
    im.alpha_composite(art.result(glow=base * .012, strength=.7)); return im

def run():
    n = 0
    def W(im, *p, q=80):
        nonlocal n; save_webp(im, *p, q=q); n += 1
    # subjects 1200x900  +  lab backgrounds 1920x1080
    names = {"physics": "physics", "chemistry": "chemistry", "biology": "biology", "mathematics": "math", "geology": "geology"}
    for k, short in names.items():
        W(subject_scene(k, 1200, 900), "03_SUBJECTS", k, f"{short}_subject.webp")
        W(subject_scene(k, 1920, 1080, dim=.55, lab=True), "04_LABORATORIES", "backgrounds", f"{short}_lab_bg.webp", q=76)
    # games 1280x720
    G = [("games_banner", 31, "purple", "#A78BFA", "games", [("trophy", 200, 1.0, 54), ("spark", -30, 1.0, 50), ("bolt" if False else "target", 20, 1.05, 46)]),
         ("daily_challenge", 32, "amber", "#FFBF69", "flame", [("calendar", 190, 1.0, 54), ("points", -20, 1.0, 50)]),
         ("science_puzzle", 33, "teal", "#35D5E8", "puzzle", [("bulb", 200, 1.0, 54), ("atom", -25, 1.0, 50)]),
         ("physics_challenge", 34, "blue", "#3987FF", "atom", [("clock", 195, 1.0, 50), ("points", -25, 1.0, 50)]),
         ("chemistry_challenge", 35, "teal", "#35D5E8", "lab", [("spark", 200, 1.0, 50), ("target", -20, 1.0, 50)]),
         ("biology_challenge", 36, "green", "#35D39A", "dna", [("check", 200, 1.0, 50), ("points", -20, 1.0, 50)]),
         ("time_challenge", 37, "red", "#FF647C", "clock", [("flame", 195, 1.0, 52), ("points", -25, 1.0, 50)]),
         ("experiment_game", 38, "purple", "#B08AFF", "bulb", [("atom", 200, 1.0, 52), ("dna", -22, 1.0, 50)])]
    for name, seed, key, acc, gl, sats in G: W(glyph_scene(1280, 720, seed, key, acc, gl, sats, rays=True), "05_GAMES", "covers", f"{name}.webp")
    # competitions
    W(glyph_scene(1920, 1080, 41, "gold", "#FFD84A", "trophy", [("award", 200, 1.0, 66), ("points", -25, 1.0, 60), ("crown", 20, 1.05, 60)], rays=True, confetti=True, disc=.27), "07_COMPETITIONS", "competition_banner.webp")
    lb = nebula(1920, 1080, 42, "purple"); a = Art(1920, 1080)
    for i in range(9): a.line([(0, 160 + i * 100), (1920, 160 + i * 100)], C("#A78BFA", 38), 2)
    for i in range(3): a.poly([(180 + i * 620, 60), (480 + i * 620, 60), (480 + i * 620, 100), (180 + i * 620, 100)], C("#FFD84A", 24 + i * 6))
    lb.alpha_composite(a.result(glow=6, strength=.4)); W(lb, "07_COMPETITIONS", "leaderboard_background.webp")
    # UI illustrations 1024x768
    U = [("onboarding_01", 51, "blue", "#3987FF", "atom", [("learn", 200, 1.0, 52), ("spark", -25, 1.0, 50)]),
         ("onboarding_02", 52, "purple", "#A78BFA", "bot", [("bulb", 200, 1.0, 52), ("help", -25, 1.0, 50)]),
         ("onboarding_03", 53, "teal", "#35D5E8", "lab", [("atom", 200, 1.0, 52), ("dna", -25, 1.0, 50)]),
         ("onboarding_04", 54, "gold", "#FFD84A", "trophy", [("award", 200, 1.0, 52), ("flame", -25, 1.0, 50)]),
         ("welcome_illustration", 55, "blue", "#35D5E8", "spark", [("atom", 200, 1.0, 52), ("learn", -25, 1.0, 50), ("trophy", 20, 1.05, 48)]),
         ("empty_courses", 56, "slate", "#8291AA", "learn", []), ("empty_downloads", 57, "slate", "#8291AA", "download2", []),
         ("empty_notifications", 58, "slate", "#8291AA", "bell", []), ("no_internet", 59, "slate", "#FFBF69", "wifioff", []),
         ("error_illustration", 60, "red", "#FF647C", "warning", []), ("success_illustration", 61, "green", "#35D39A", "check", [("spark", 200, 1.0, 46), ("points", -25, 1.0, 44)]),
         ("loading_illustration", 62, "blue", "#3987FF", "repeat", [])]
    for name, seed, key, acc, gl, sats in U: W(glyph_scene(1024, 768, seed, key, acc, gl, sats, disc=.27), "08_UI_ILLUSTRATIONS", f"{name}.webp")
    # study & analytics 1024x768
    A = [("study_planner", 71, "blue", "#3987FF", "calendar", None), ("weekly_report", 72, "purple", "#A78BFA", "bars", None), ("learning_progress", 73, "green", "#35D39A", "target", .72),
         ("student_analytics", 74, "teal", "#35D5E8", "chart", None), ("study_calendar", 75, "blue", "#35D5E8", "clock", None), ("digital_notebook", 76, "amber", "#FFBF69", "note", None),
         ("revision_mode", 77, "purple", "#B08AFF", "repeat", None), ("focus_mode", 78, "teal", "#35D5E8", "target", None)]
    for name, seed, key, acc, gl, pr in A: W(glyph_scene(1024, 768, seed, key, acc, gl, progress=pr, disc=.27), "09_STUDY_ANALYTICS", f"{name}.webp")
    # subscriptions
    W(glyph_scene(1920, 1080, 81, "gold", "#FFD84A", "crown", [("points", 200, 1.0, 60), ("award", -25, 1.0, 58), ("spark", 20, 1.05, 54)], rays=True, disc=.25), "10_SUBSCRIPTIONS", "subscription_banner.webp")
    W(glyph_scene(1920, 1080, 82, "purple", "#A78BFA", "check", [("bot", 200, 1.0, 60), ("lab", -25, 1.0, 58), ("download", 20, 1.05, 54)], disc=.25), "10_SUBSCRIPTIONS", "premium_features.webp")
    # website + dashboards 1920x1080
    W(glyph_scene(1920, 1080, 91, "blue", "#35D5E8", "atom", [("bot", 200, 1.0, 64), ("lab", -25, 1.0, 60), ("trophy", 20, 1.05, 58), ("learn", 155, 1.1, 56)], rays=True, disc=.28), "11_WEBSITE", "website_hero.webp")
    W(glyph_scene(1920, 1080, 92, "purple", "#A78BFA", "spark", [("bot", 200, 1.0, 60), ("lab", -25, 1.0, 58), ("games", 20, 1.05, 56), ("chart", 155, 1.1, 54)], disc=.25), "11_WEBSITE", "website_features.webp")
    W(glyph_scene(1920, 1080, 93, "teal", "#35D5E8", "lab", [("atom", 200, 1.0, 60), ("dna", -25, 1.0, 58)], disc=.27), "11_WEBSITE", "website_labs.webp")
    W(glyph_scene(1920, 1080, 94, "purple", "#B08AFF", "bot", [("bulb", 200, 1.0, 60), ("help", -25, 1.0, 58)], disc=.27), "11_WEBSITE", "website_ai_teacher.webp")
    for name, seed, key in (("admin_dashboard_bg", 95, "slate"), ("teacher_dashboard_bg", 96, "teal")):
        im = nebula(1920, 1080, seed, key, stars=900); g = Art(1920, 1080)
        for i in range(0, 1920, 96): g.line([(i, 0), (i, 1080)], C("#35D5E8", 14), 1)
        for j in range(0, 1080, 96): g.line([(0, j), (1920, j)], C("#35D5E8", 14), 1)
        im.alpha_composite(g.result()); W(im, "11_WEBSITE", f"{name}.webp")
    return n
if __name__ == "__main__": print(run(), "scene images")
