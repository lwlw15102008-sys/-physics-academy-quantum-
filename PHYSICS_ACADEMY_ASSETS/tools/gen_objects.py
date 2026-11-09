"""Transparent object PNGs: lab equipment, trophies, medals, badges, podiums, game objects, plans."""
import random
from toolkit import *

def canvas(w=512, h=512): return Image.new("RGBA", (w, h), (0, 0, 0, 0))
def gp(img, pts, top, bottom, mid=None, alpha=255, mode="v"):
    img.alpha_composite(grad_poly(img.size, pts, top, bottom, mid, alpha=alpha, mode=mode))
def shadow(img, cx, cy, rx, ry, a=90):
    s = Art(*img.size); s.circle(cx, cy, 1, fill=(0, 0, 0, 0)); lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, a)); img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(ry * .6)))
def glow(img, art_img, radius, k=1.0):
    r, g, b, a = art_img.filter(ImageFilter.GaussianBlur(radius)).split(); a = a.point(lambda v: int(min(255, v * k)))
    img.alpha_composite(Image.merge("RGBA", (r, g, b, a)))
def tube_pts(x, y, w, h):
    r = w / 2; return [(x, y), (x + w, y)] + arc_pts(x + r, y + h - r, r, 0, 180)[::1] + []
def glass_tube(img, x, top, w, h, liquid, level=.6, lip=True):
    r = w / 2; body = [(x, top), (x + w, top)] + arc_pts(x + r, top + h - r, r, 0, 180)
    gp(img, body, "#DDEBFF", "#9FB8DA", alpha=70)
    ly = top + h * (1 - level); liq = [(x + 2, ly), (x + w - 2, ly)] + arc_pts(x + r, top + h - r, r - 2, 0, 180)
    gp(img, liq, liquid, shade_hex(liquid, .6), alpha=235)
    a = Art(*img.size, ss=3); a.line(body + [body[0]], C("#EAF4FF", 210), 2.5); a.line([(x + w * .22, top + 8), (x + w * .22, top + h * .7)], C("#FFFFFF", 150), 3)
    if lip: a.line([(x - 4, top), (x + w + 4, top)], C("#EAF4FF", 230), 3.5)
    img.alpha_composite(a.result())
def shade_hex(h, f):
    r, g, b = hexrgb(h); return "#%02X%02X%02X" % (int(r * f), int(g * f), int(b * f))

# ───────── lab equipment ─────────
def lab_table():
    im = canvas(); shadow(im, 256, 470, 220, 18)
    gp(im, [(60, 215), (452, 215), (500, 262), (12, 262)], "#4A5F8A", "#2E3F61")
    gp(im, [(12, 262), (500, 262), (500, 292), (12, 292)], "#1F2D4A", "#141D33")
    for x in (40, 432): gp(im, [(x, 292), (x + 40, 292), (x + 40, 462), (x, 462)], "#24324F", "#121A2E")
    gp(im, [(80, 392), (432, 392), (432, 412), (80, 412)], "#1B2641", "#101828")
    a = Art(512, 512, 3); a.line([(60, 215), (452, 215), (500, 262), (12, 262), (60, 215)], C("#35D5E8", 210), 3); a.line([(12, 292), (500, 292)], C("#35D5E8", 150), 2); im.alpha_composite(a.result(glow=6, strength=.5)); return im

def test_tubes():
    im = canvas(); shadow(im, 256, 440, 190, 14)
    cols = ["#FF647C", "#35D5E8", "#A6F36B", "#FFD84A", "#B08AFF"]; levels = [.55, .7, .45, .62, .5]
    for i in range(5): glass_tube(im, 92 + i * 66, 120 + (i % 2) * 14, 40, 280 - (i % 2) * 14, cols[i], levels[i])
    gp(im, [(60, 300), (452, 300), (452, 322), (60, 322)], "#4A5F8A", "#2E3F61"); gp(im, [(60, 322), (452, 322), (452, 345), (60, 345)], "#1F2D4A", "#141D33")
    return im

def lab_glassware():
    im = canvas(); shadow(im, 256, 452, 210, 14)
    # beaker
    b = [(60, 190), (200, 190), (192, 420), (68, 420)]; gp(im, b, "#DDEBFF", "#9FB8DA", alpha=70)
    gp(im, [(66, 300), (194, 300), (192, 418), (68, 418)], "#35D5E8", "#1B7FA0", alpha=225)
    # flask
    f = [(300, 150), (350, 150), (350, 250), (420, 420), (230, 420), (300, 250)]; gp(im, f, "#DDEBFF", "#9FB8DA", alpha=70)
    gp(im, [(270, 340), (410, 340), (420, 418), (232, 418)], "#FF647C", "#A82B45", alpha=225)
    # cylinder
    gp(im, [(430, 120), (480, 120), (480, 420), (430, 420)], "#DDEBFF", "#9FB8DA", alpha=70); gp(im, [(432, 270), (478, 270), (478, 418), (432, 418)], "#A6F36B", "#5DAA2B", alpha=225)
    a = Art(512, 512, 3)
    for pts in (b + [b[0]], f + [f[0]], [(430, 120), (480, 120), (480, 420), (430, 420), (430, 120)]): a.line(pts, C("#EAF4FF", 215), 3)
    for y in range(140, 410, 30): a.line([(430, y), (445, y)], C("#EAF4FF", 190), 2)
    a.line([(80, 205), (84, 400)], C("#FFFFFF", 140), 4); a.line([(312, 160), (312, 240)], C("#FFFFFF", 140), 4); im.alpha_composite(a.result()); return im

def electrical_components():
    im = canvas(); a = Art(512, 512, 3)
    # resistor
    a.line([(30, 120), (150, 120)], C("#CBD5E8"), 6); a.poly(rrect_pts(150, 96, 120, 48, 22), C("#E6C79A")); a.poly(rrect_pts(150, 96, 120, 48, 22), C("#E6C79A"))
    for x, col in ((172, "#B3261E"), (196, "#111111"), (220, "#FFB800"), (244, "#C0C0C0")): a.poly([(x, 98), (x + 10, 98), (x + 10, 142), (x, 142)], C(col))
    a.line([(270, 120), (390, 120)], C("#CBD5E8"), 6)
    # LED
    a.circle(150, 270, 52, fill=C("#FF647C", 230)); a.poly([(98, 270), (202, 270), (202, 330), (98, 330)], C("#FF647C", 230)); a.poly([(88, 330), (212, 330), (212, 342), (88, 342)], C("#B3261E"))
    a.line([(125, 342), (125, 420)], C("#CBD5E8"), 5); a.line([(175, 342), (175, 400)], C("#CBD5E8"), 5); a.line([(124, 235), (138, 258)], C("#FFFFFF", 170), 6)
    # switch
    a.poly(rrect_pts(290, 260, 170, 110, 16), C("#2A3A5C")); a.circle(330, 315, 12, fill=C("#CBD5E8")); a.circle(430, 315, 12, fill=C("#CBD5E8")); a.line([(330, 315), (410, 268)], C("#FFD84A"), 9)
    # capacitor
    a.poly(rrect_pts(300, 395, 54, 85, 8), C("#35D5E8")); a.poly([(300, 395), (354, 395), (354, 410), (300, 410)], C("#1B7FA0")); a.line([(318, 480), (318, 500)], C("#CBD5E8"), 4); a.line([(336, 480), (336, 500)], C("#CBD5E8"), 4)
    base = a.result(); im.alpha_composite(base)
    g = Art(512, 512, 2); g.circle(150, 270, 58, fill=C("#FF647C", 120)); glow(im, g.result(), 22, 1.0); im.alpha_composite(base.crop((60, 190, 240, 345)), (60, 190)); return im

def wires_batteries():
    im = canvas(); shadow(im, 256, 455, 200, 14); a = Art(512, 512, 3)
    for i, x in enumerate((110, 250)):
        a.poly(rrect_pts(x, 150, 90, 270, 18), C("#1B2740")); a.poly(rrect_pts(x, 190, 90, 190, 4), C("#35D39A" if i == 0 else "#FFB800")); a.poly(rrect_pts(x + 28, 130, 34, 24, 6), C("#CBD5E8"))
        a.line([(x + 45, 250), (x + 45, 300)], C("#0B1426"), 10); a.line([(x + 20, 275), (x + 70, 275)], C("#0B1426"), 10)
    for k, col in enumerate(("#FF647C", "#35D5E8")):
        pts = [(x, 110 + k * 8 + 26 * math.sin(rad(x * 1.2 + k * 80))) for x in range(40, 470, 6)]; a.line(pts, C(col), 11)
    a.line([(380, 200), (470, 200), (470, 380), (380, 380)], C("#FFD84A"), 10); a.poly(rrect_pts(380, 190, 60, 20, 6), C("#CBD5E8")); im.alpha_composite(a.result()); return im

def microscope():
    im = canvas(); shadow(im, 256, 470, 170, 14); a = Art(512, 512, 3)
    a.poly(rrect_pts(120, 430, 270, 36, 14), C("#2B3B5E")); a.line([(190, 430), (200, 300), (250, 190), (320, 150)], C("#4A6AA8"), 34)
    a.poly(rrect_pts(150, 330, 190, 20, 6), C("#CBD5E8")); gt = [(250, 80), (290, 70), (360, 225), (320, 240)]; a.poly(gt, C("#5C7CC0")); a.poly([(296, 210), (344, 195), (352, 245), (305, 258)], C("#CBD5E8"))
    a.poly([(238, 40), (278, 28), (290, 70), (250, 82)], C("#35D5E8")); a.circle(330, 262, 14, fill=C("#1B2740")); im.alpha_composite(a.result(glow=4, strength=.3)); return im

def cell_model():
    im = canvas(); shadow(im, 256, 470, 190, 14); lay = Art(512, 512, 3)
    lay.d.ellipse([40 * 3, 70 * 3, 472 * 3, 440 * 3], fill=C("#35D39A", 70), outline=C("#7DF0C4", 230), width=9)
    lay.d.ellipse([200 * 3, 170 * 3, 340 * 3, 300 * 3], fill=C("#8957FF", 235)); lay.d.ellipse([245 * 3, 215 * 3, 290 * 3, 255 * 3], fill=C("#F04FB5"))
    for (x, y) in ((100, 200), (400, 330), (120, 340), (380, 160)): lay.d.ellipse([(x - 30) * 3, (y - 16) * 3, (x + 30) * 3, (y + 16) * 3], fill=C("#FF9F6B", 235)); lay.line([(x - 18, y), (x - 6, y - 7), (x + 6, y + 7), (x + 18, y)], C("#FFD9B8"), 2.5)
    lay.line([(80, 290), (110, 270), (140, 300), (170, 280), (200, 310)], C("#FFD84A"), 5)
    rnd = random.Random(3)
    for _ in range(34): x, y = rnd.uniform(70, 440), rnd.uniform(110, 410); lay.circle(x, y, 4, fill=C("#B8FFF0", 220)) if (x - 256) ** 2 / 190 ** 2 + (y - 255) ** 2 / 165 ** 2 < .8 else None
    im.alpha_composite(lay.result(glow=5, strength=.35)); return im

def dna_model():
    im = canvas(); a = Art(512, 512, 3); n = 80; sa, sb = [], []
    for i in range(n + 1):
        t = i / n; y = 30 + 452 * t; ph = rad(t * 900); sa.append((256 + 95 * math.sin(ph), y)); sb.append((256 - 95 * math.sin(ph), y))
        if i % 4 == 0: a.line([sa[-1], sb[-1]], C("#EAF4FF", 150), 5)
    a.line(sa, C("#35D5E8"), 13); a.line(sb, C("#F04FB5"), 13)
    for i in range(0, n + 1, 4): a.circle(*sa[i], 9, fill=C("#FFFFFF")); a.circle(*sb[i], 9, fill=C("#FFFFFF"))
    im.alpha_composite(a.result(glow=6, strength=.4)); return im

# ───────── trophies / medals ─────────
TIERS = {"gold": ("#FFF1A8", "#FFC93A", "#9A6A0C"), "silver": ("#F4F6FA", "#BCC5D3", "#6B7686"), "bronze": ("#F7C9A0", "#D98A4E", "#7A4420"),
         "blue": ("#CFE3FF", "#4E8DFF", "#1B3F9E"), "purple": ("#E3D4FF", "#9B6BFF", "#4C23A8")}
def trophy(tier, number=None, size=512, with_glow=False):
    lt, md, dk = TIERS[tier]; im = canvas(size, size); k = size / 512; shadow(im, 256 * k, 482 * k, 130 * k, 12 * k)
    if with_glow:
        g = Art(size, size, 2); g.circle(256 * k, 230 * k, 150 * k, fill=C(md, 120)); glow(im, g.result(), 40 * k, 1.0)
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    for side in (-1, 1):
        hx = [(256 + side * (110 + 60 * math.sin(rad(t))), 120 + 80 * (t / 180) * 1.0 + 0) for t in range(0, 181, 12)]
        a = Art(size, size, 3); a.line(P(hx), C(dk), 22 * k); a.line(P(hx), C(md), 14 * k); im.alpha_composite(a.result())
    cup = [(150, 70), (362, 70), (352, 190)] + [(256 + 96 * math.cos(rad(a_)), 190 + 96 * math.sin(rad(a_))) for a_ in range(0, 181, 10)] + [(160, 190)]
    gp(im, P(cup), lt, dk, md); gp(im, P([(256, 286), (256, 286), (290, 286), (290, 360), (222, 360), (222, 286)]), md, dk)
    gp(im, P([(190, 360), (322, 360), (338, 400), (174, 400)]), md, dk); gp(im, P([(150, 400), (362, 400), (362, 440), (150, 440)]), lt, dk, md)
    a = Art(size, size, 3); a.line(P([(190, 90), (196, 180)]), C("#FFFFFF", 170), 10 * k); im.alpha_composite(a.result())
    if number is not None:
        d = ImageDraw.Draw(im); d.text((256 * k, 134 * k), str(number), font=font(110 * k), fill=C(dk), anchor="mm", stroke_width=int(3 * k), stroke_fill=C(lt))
    return im

def medal(tier, size=512):
    lt, md, dk = TIERS[tier]; im = canvas(size, size); k = size / 512; shadow(im, 256 * k, 480 * k, 100 * k, 10 * k)
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    gp(im, P([(170, 20), (250, 20), (290, 230), (210, 230)]), "#4E8DFF", "#1B3F9E"); gp(im, P([(342, 20), (262, 20), (222, 230), (302, 230)]), "#FF647C", "#9E1F3A")
    disc = [(256 + 150 * math.cos(rad(a)), 320 + 150 * math.sin(rad(a))) for a in range(0, 360, 5)]; gp(im, P(disc), lt, dk, md)
    inner = [(256 + 112 * math.cos(rad(a)), 320 + 112 * math.sin(rad(a))) for a in range(0, 360, 5)]; gp(im, P(inner), dk, md)
    a = Art(size, size, 3); a.poly(P(star_pts(256, 322, 70, 30)), C(lt)); a.line(P(inner + [inner[0]]), C(lt, 200), 4 * k); im.alpha_composite(a.result()); return im

def podium(place):
    im = canvas(); heights = {1: 300, 2: 220, 3: 160}; cols = {1: "gold", 2: "silver", 3: "bronze"}; lt, md, dk = TIERS[cols[place]]; h = heights[place]; top = 470 - h
    shadow(im, 256, 478, 190, 12)
    gp(im, [(90, top), (422, top), (422, 470), (90, 470)], md, dk); gp(im, [(90, top), (422, top), (440, top - 22), (108, top - 22)], lt, md); gp(im, [(422, top), (440, top - 22), (440, 448), (422, 470)], dk, shade_hex(dk, .6))
    d = ImageDraw.Draw(im); d.text((256, top + h * .45), str(place), font=font(150), fill=C("#FFFFFF", 235), anchor="mm", stroke_width=4, stroke_fill=C(dk))
    if place == 1: a = Art(512, 512, 3); a.glyph("crown", 256, top - 70, 100, C(lt), 2.2); im.alpha_composite(a.result(glow=8, strength=.6))
    return im

# ───────── badges ─────────
BADGES = [("badge_physics_genius", "atom", "blue", "poly6"), ("badge_chemistry_scientist", "lab", "silver", "poly8"), ("badge_biology_expert", "dna", "bronze", "poly6"),
          ("badge_first_lesson", "learn", "gold", "shield"), ("badge_first_unit", "level", "silver", "shield"), ("badge_100_problems", "100", "gold", "circle"),
          ("badge_concept_mastery", "target", "purple", "poly8"), ("badge_experiment_complete", "check", "blue", "poly6"), ("badge_learning_streak", "flame", "bronze", "circle"),
          ("badge_daily_challenge", "calendar", "gold", "poly8"), ("badge_quiz_excellence", "points", "purple", "shield"), ("badge_regular_review", "repeat", "silver", "circle")]
def badge_shape(kind):
    if kind == "circle": return [(256 + 220 * math.cos(rad(a)), 256 + 220 * math.sin(rad(a))) for a in range(0, 360, 4)]
    if kind == "poly6": return [(256 + 225 * math.cos(rad(60 * i - 90)), 256 + 225 * math.sin(rad(60 * i - 90))) for i in range(6)]
    if kind == "poly8": return [(256 + 225 * math.cos(rad(45 * i - 67.5)), 256 + 225 * math.sin(rad(45 * i - 67.5))) for i in range(8)]
    right = [(256 + 190 * math.cos(rad(a)) * 1.0, 250 + 205 * math.sin(rad(a))) for a in range(0, 91, 6)]
    return [(66, 60), (256, 36), (446, 60), (446, 250)] + [(256 + 190 * math.cos(rad(a)), 250 + 215 * math.sin(rad(a))) for a in range(0, 91, 6)][1:] + [(256 - 190 * math.cos(rad(a)), 250 + 215 * math.sin(rad(a))) for a in range(90, -1, -6)][:-1]
def badge(name, glyph, tier, shape):
    lt, md, dk = TIERS[tier]; im = canvas(); pts = badge_shape(shape); sh = Art(512, 512, 2); shadow(im, 256, 470, 170, 12)
    gp(im, pts, lt, dk, md); c = (256, 256); inner = [(c[0] + (x - c[0]) * .8, c[1] + (y - c[1]) * .8) for x, y in pts]; gp(im, inner, shade_hex(dk, .8), shade_hex(md, .85))
    a = Art(512, 512, 3); a.line(inner + [inner[0]], C(lt, 180), 4)
    if glyph == "100": im.alpha_composite(a.result()); ImageDraw.Draw(im).text((256, 262), "100", font=font(120), fill=C("#FFFFFF"), anchor="mm", stroke_width=5, stroke_fill=C(shade_hex(dk, .45)))
    else: a.glyph(glyph, 256, 256, 210, C("#FFFFFF"), 2.3); im.alpha_composite(a.result(glow=5, strength=.4))
    return im

def game_objects():
    # mystery box
    im = canvas(); shadow(im, 256, 470, 170, 14)
    gp(im, [(256, 70), (440, 160), (256, 250), (72, 160)], "#C9B0FF", "#8B63F0"); gp(im, [(72, 160), (256, 250), (256, 450), (72, 360)], "#7B52E8", "#4325A8"); gp(im, [(440, 160), (256, 250), (256, 450), (440, 360)], "#5B3AC4", "#2F1A80")
    a = Art(512, 512, 3); a.glyph("help", 164, 310, 120, C("#FFFFFF", 235), 2.6); a.line([(72, 160), (256, 250), (440, 160)], C("#E9DFFF", 200), 4); a.line([(256, 250), (256, 450)], C("#E9DFFF", 160), 4)
    a.glyph("spark", 380, 80, 60, C("#FFD84A"), 2); a.glyph("spark", 90, 90, 40, C("#35D5E8"), 2); im.alpha_composite(a.result(glow=10, strength=.6)); box = im
    vic = canvas(); comp(vic, trophy("gold", None, 420, with_glow=True), 46, 84); a = Art(512, 512, 3)
    for x, y, r in ((112, 96, 38), (256, 56, 48), (400, 96, 38)): a.poly(star_pts(x, y, r, r * .42), C("#FFD84A"))
    vic.alpha_composite(a.result(glow=6, strength=.5))
    rt = canvas(); a = Art(512, 512, 3); g = Art(512, 512, 2); g.circle(256, 256, 190, fill=C("#3987FF", 110)); glow(rt, g.result(), 34, 1.0)
    a.circle(256, 256, 170, fill=C("#0A1226", 235), outline=C("#35D5E8"), width=8); a.glyph("repeat", 256, 256, 210, C("#FFFFFF"), 2.5); rt.alpha_composite(a.result(glow=6, strength=.4))
    return box, vic, rt

def winner_celebration():
    im = canvas(1024, 1024); t = trophy("gold", 1, 760, with_glow=True); comp(im, t, 132, 200); rnd = random.Random(9); a = Art(1024, 1024, 2)
    for _ in range(140):
        x, y = rnd.uniform(0, 1024), rnd.uniform(0, 1024); col = rnd.choice(["#FFD84A", "#35D5E8", "#F04FB5", "#A78BFA", "#35D39A", "#FF9F6B"]); th = rnd.uniform(0, 6.28); L = rnd.uniform(14, 34)
        a.line([(x, y), (x + L * math.cos(th), y + L * math.sin(th))], C(col), rnd.uniform(5, 10))
    comp(im, a.result(), 0, 0); return im

def plan_card(tier, glyph, accent, rows=4):
    im = canvas(768, 1024); lt, md, dk = TIERS[tier]; card = rrect_pts(24, 24, 720, 976, 56)
    g = Art(768, 1024, 2); g.poly(card, C(accent, 140)); glow(im, g.result(), 24, 1.0)
    gp(im, card, "#18274A", "#0B1226", alpha=250); a = Art(768, 1024, 3); a.line(card + [card[0]], C(accent, 255), 6)
    a.circle(384, 250, 130, fill=C("#0A1226", 255), outline=C(accent, 255), width=7); a.glyph(glyph, 384, 250, 150, C("#FFFFFF"), 2.3)
    for i in range(rows):
        y = 470 + i * (400 // rows); a.circle(130, y, 20, outline=C(accent, 255), width=5); a.line([(122, y), (128, y + 7), (140, y - 8)], C(accent, 255), 4); a.line([(190, y), (620 - i * 40, y)], C("#8291AA", 170), 14)
    a.poly(rrect_pts(150, 880, 468, 80, 40), C(accent, 255)); im.alpha_composite(a.result(glow=4, strength=.3)); return im

def avatar_default():
    im = canvas(); a = Art(512, 512, 3); gp(im, [(256 + 250 * math.cos(rad(t)), 256 + 250 * math.sin(rad(t))) for t in range(0, 360, 4)], "#3987FF", "#8957FF", mode="d")
    a.circle(256, 205, 78, fill=C("#EAF2FF")); a.poly([(96, 540)] + [(256 + 160 * math.cos(rad(t)), 440 + 130 * math.sin(rad(t))) for t in range(180, 361, 6)] + [(416, 540)], C("#EAF2FF"))
    mask = Image.new("L", (512, 512), 0); ImageDraw.Draw(mask).ellipse([6, 6, 506, 506], fill=255); art = a.result(); lay = Image.new("RGBA", (512, 512), (0, 0, 0, 0)); lay.paste(art, (0, 0), mask); im.alpha_composite(lay); return im

def run():
    n = 0
    def P(im, *p):
        nonlocal n; save_png(im, *p); n += 1
    P(lab_table(), "04_LABORATORIES", "backgrounds", "lab_table.png")
    P(test_tubes(), "04_LABORATORIES", "chemistry", "test_tubes.png"); P(lab_glassware(), "04_LABORATORIES", "chemistry", "lab_glassware.png")
    P(electrical_components(), "04_LABORATORIES", "physics", "electrical_components.png"); P(wires_batteries(), "04_LABORATORIES", "physics", "wires_batteries.png")
    P(microscope(), "04_LABORATORIES", "biology", "microscope.png"); P(cell_model(), "04_LABORATORIES", "biology", "cell_model.png"); P(dna_model(), "04_LABORATORIES", "biology", "dna_model.png")
    for i, t in enumerate(("gold", "silver", "bronze", "blue", "purple"), 1): P(trophy(t, i), "06_REWARDS", "trophies", f"trophy_rank_{i}.png")
    for t in ("gold", "silver", "bronze"): P(medal(t), "06_REWARDS", "medals", f"medal_{t}.png")
    for name, g, tier, shape in BADGES: P(badge(name, g, tier, shape), "06_REWARDS", "badges", f"{name}.png")
    for i in (1, 2, 3): P(podium(i), "07_COMPETITIONS", f"podium_{('first', 'second', 'third')[i - 1]}.png")
    P(medal("gold"), "07_COMPETITIONS", "competition_medal.png"); P(winner_celebration(), "07_COMPETITIONS", "winner_celebration.png")
    box, vic, rt = game_objects(); P(box, "05_GAMES", "objects", "mystery_box.png"); P(vic, "05_GAMES", "objects", "game_victory.png"); P(rt, "05_GAMES", "objects", "game_retry.png")
    P(plan_card("silver", "user", "#8FA3C4"), "10_SUBSCRIPTIONS", "plan_free.png"); P(plan_card("blue", "bot", "#35D5E8"), "10_SUBSCRIPTIONS", "plan_pro.png"); P(plan_card("gold", "crown", "#FFD84A", 5), "10_SUBSCRIPTIONS", "plan_vip.png")
    P(avatar_default(), "08_UI_ILLUSTRATIONS", "student_profile_default.png")
    return n
if __name__ == "__main__": print(run(), "object images")
