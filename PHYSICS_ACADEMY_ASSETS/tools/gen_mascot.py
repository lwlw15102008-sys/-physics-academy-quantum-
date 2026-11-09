"""AI teacher mascot 'Quanta' — a friendly 2D robot teacher drawn procedurally. Same character in every image; only face and pose change."""
import random
from toolkit import *
from gen_objects import canvas, gp, glow, shadow, comp

CY = "#35D5E8"
POSES = {
    "main":           dict(eyes="round", mouth="smile", L=None, R=None),
    "happy":          dict(eyes="happy", mouth="grin", R=[(640, 530), (740, 470), (790, 360)], fx="wave"),
    "explaining":     dict(eyes="round", mouth="open", R=[(640, 530), (760, 580), (850, 540)], fx="holo"),
    "thinking":       dict(eyes="up", mouth="line", R=[(640, 530), (700, 620), (584, 478)], fx="think", front_r=True),
    "pointing":       dict(eyes="round", mouth="smile", R=[(640, 530), (770, 480), (860, 380)], fx="board"),
    "congratulations": dict(eyes="happy", mouth="grin", L=[(384, 530), (280, 440), (250, 310)], R=[(640, 530), (744, 440), (774, 310)], fx="party"),
    "guidance":       dict(eyes="round", mouth="smile", R=[(640, 530), (780, 550), (900, 520)], fx="arrow"),
    "listening":      dict(eyes="wide", mouth="o", R=[(640, 530), (742, 440), (704, 336)], tilt=-8, fx="sound", front_r=True),
}
DEF_L = [(384, 530), (340, 640), (352, 738)]; DEF_R = [(640, 530), (684, 640), (672, 738)]

def arm(im, pts):
    a = Art(1024, 1024, 2); a.line(pts, C("#8FA2C9"), 50); a.line(pts, C("#D9E3F7"), 32); a.circle(*pts[-1], 31, fill=C("#8FA2C9")); a.circle(*pts[-1], 26, fill=C("#EAF0FC"))
    a.circle(pts[-1][0] - 8, pts[-1][1] - 8, 8, fill=C("#FFFFFF", 180)); im.alpha_composite(a.result())

def head(pose):
    im = canvas(1024, 1024)
    for x in (316, 684): gp(im, rrect_pts(x, 288, 24, 86, 10), "#9FB0D3", "#6E80A8")
    gp(im, rrect_pts(340, 190, 344, 282, 96), "#FFFFFF", "#AFBEDD", "#DCE5F6"); gp(im, rrect_pts(372, 246, 280, 176, 72), "#0B1330", "#050914")
    a = Art(1024, 1024, 2); a.line(rrect_pts(372, 246, 280, 176, 72) + [(372 + 72, 246)], C(CY, 150), 4)
    # cap (teacher)
    a.poly([(404, 214), (620, 214), (620, 248), (512, 266), (404, 248)], C("#14213F")); a.poly([(512, 126), (704, 186), (512, 248), (320, 186)], C("#22346B"))
    a.line([(512, 126), (704, 186), (512, 248), (320, 186)], C(CY, 220), 4, closed=True); a.line([(700, 190), (716, 268)], C("#FFD84A"), 5); a.circle(716, 276, 10, fill=C("#FFD84A"))
    eyes, mouth = pose["eyes"], pose["mouth"]; ex = (452, 572); ey = 318
    for x in ex:
        if eyes in ("round", "up", "wide"):
            r = 29 if eyes == "wide" else 24; dx, dy = (7, -9) if eyes == "up" else (0, 0)
            a.circle(x + dx, ey + dy, r, fill=C(CY)); a.circle(x + dx - 7, ey + dy - 8, 7, fill=C("#FFFFFF", 235))
        else: a.line(arc_pts(x, ey + 14, 26, 205, 335), C(CY), 10)
    mx, my = 512, 378
    if mouth == "smile": a.line(arc_pts(mx, my - 26, 40, 35, 145), C(CY), 8)
    elif mouth == "grin": a.poly(arc_pts(mx, my - 20, 44, 5, 175) + [(mx - 44 * math.cos(rad(5)), my - 20 + 44 * math.sin(rad(5)))], C(CY))
    elif mouth == "open": a.poly(ell_pts(mx, my - 4, 22, 16, 0), C(CY)); a.poly(ell_pts(mx, my + 1, 12, 7, 0), C("#0B1330"))
    elif mouth == "line": a.line([(mx - 22, my - 4), (mx + 22, my - 8)], C(CY), 8)
    elif mouth == "o": a.circle(mx, my - 4, 14, outline=C(CY), width=7)
    im.alpha_composite(a.result(glow=5, strength=.5)); return im

def robot(name):
    p = POSES[name]; im = canvas(1024, 1024); shadow(im, 512, 884, 190, 18)
    for x in (430, 534): gp(im, rrect_pts(x, 748, 60, 120, 24), "#31456F", "#1B2740")
    a = Art(1024, 1024, 2); a.poly(ell_pts(460, 880, 48, 20), C("#14213F")); a.poly(ell_pts(564, 880, 48, 20), C("#14213F")); im.alpha_composite(a.result())
    gp(im, rrect_pts(482, 462, 60, 40, 10), "#AFBEDD", "#6E80A8"); gp(im, rrect_pts(372, 490, 280, 272, 74), "#6FA6FF", "#1E4FA8", "#3987FF")
    a = Art(1024, 1024, 2); a.circle(512, 618, 54, fill=C("#0B1330"), outline=C(CY, 240), width=6); a.glyph("atom", 512, 618, 64, C("#FFFFFF"), 2)
    a.line(rrect_pts(396, 520, 232, 214, 56) + [(396 + 56, 520)], C("#FFFFFF", 50), 4); im.alpha_composite(a.result(glow=6, strength=.5))
    arm(im, p.get("L") or DEF_L)
    if not p.get("front_r"): arm(im, p.get("R") or DEF_R)
    fx = p.get("fx"); h = head(p)
    if p.get("tilt"): h = h.rotate(p["tilt"], resample=Image.BICUBIC, center=(512, 470))
    im.alpha_composite(h)
    a = Art(1024, 1024, 2); a.poly([(512, 500), (466, 474), (466, 526)], C("#8957FF")); a.poly([(512, 500), (558, 474), (558, 526)], C("#8957FF")); a.circle(512, 500, 13, fill=C("#B08AFF")); im.alpha_composite(a.result())
    if p.get("front_r"): arm(im, p["R"])
    f = Art(1024, 1024, 2); rnd = random.Random(4)
    if fx == "holo":
        f.circle(905, 430, 92, fill=C(CY, 40), outline=C(CY, 200), width=4); f.glyph("atom", 905, 430, 110, C("#FFFFFF"), 2); im.alpha_composite(f.result(glow=10, strength=.8))
    elif fx == "think":
        for x, y, r in ((730, 200, 10), (770, 150, 15), (825, 90, 22)): f.circle(x, y, r, fill=C("#FFFFFF", 235))
        f.circle(880, 90, 50, fill=C("#0B1330", 240), outline=C(CY, 230), width=5); f.glyph("help", 880, 90, 64, C(CY), 2.3); im.alpha_composite(f.result(glow=8, strength=.6))
    elif fx == "board":
        f.poly(rrect_pts(780, 130, 220, 190, 22), C("#0B1330", 245)); f.line(rrect_pts(780, 130, 220, 190, 22) + [(802, 130)], C(CY, 230), 5)
        for i, hh in enumerate((70, 110, 50, 130)): f.poly([(808 + i * 48, 296), (840 + i * 48, 296), (840 + i * 48, 296 - hh), (808 + i * 48, 296 - hh)], C(("#35D5E8", "#A78BFA", "#35D39A", "#FFD84A")[i]))
        f.line([(860, 380), (905, 332)], C("#EAF0FC"), 14); im.alpha_composite(f.result(glow=6, strength=.5))
    elif fx == "party":
        for _ in range(60):
            x, y = rnd.uniform(40, 984), rnd.uniform(30, 520); th = rnd.uniform(0, 6.28); L = rnd.uniform(14, 30); f.line([(x, y), (x + L * math.cos(th), y + L * math.sin(th))], C(rnd.choice(["#FFD84A", CY, "#F04FB5", "#A78BFA", "#35D39A"])), rnd.uniform(5, 9))
        f.poly(star_pts(512, 60, 44, 18), C("#FFD84A")); im.alpha_composite(f.result(glow=6, strength=.5))
    elif fx == "arrow":
        f.circle(935, 470, 60, fill=C("#0B1330", 240), outline=C(CY, 230), width=5); f.glyph("back", 935, 470, 74, C(CY), 2.5); im.alpha_composite(f.result(glow=8, strength=.6))
    elif fx == "sound":
        for r in (34, 58, 82): f.line(arc_pts(744, 336, r, -48, 48), C(CY, 230), 8)
        im.alpha_composite(f.result(glow=6, strength=.5))
    elif fx == "wave":
        for r in (26, 46): f.line(arc_pts(790, 360, r, 200, 340), C("#FFD84A", 230), 7)
        im.alpha_composite(f.result(glow=4, strength=.4))
    return im

def run():
    n = 0
    for name in POSES:
        im = robot(name); sub, fn = (("characters", "teacher_main.png") if name == "main" else ("expressions", f"teacher_{name}.png")); save_png(im, "02_AI_TEACHER", sub, fn); n += 1
        if name == "main":
            h = im.crop((284, 100, 740, 556)).resize((512, 512), Image.LANCZOS); save_png(h, "02_AI_TEACHER", "avatars", "teacher_avatar.png"); n += 1
            bg = canvas(512, 512); gp(bg, [(256 + 254 * math.cos(rad(t)), 256 + 254 * math.sin(rad(t))) for t in range(0, 360, 4)], "#3987FF", "#8957FF", mode="d")
            mask = Image.new("L", (512, 512), 0); ImageDraw.Draw(mask).ellipse([2, 2, 510, 510], fill=255); face = h.resize((440, 440), Image.LANCZOS); lay = canvas(512, 512); lay.alpha_composite(face, (36, 56))
            lay2 = canvas(512, 512); lay2.paste(lay, (0, 0), mask); bg.alpha_composite(lay2); save_png(bg, "02_AI_TEACHER", "avatars", "teacher_profile.png"); n += 1
    return n
if __name__ == "__main__": print(run(), "mascot images")
