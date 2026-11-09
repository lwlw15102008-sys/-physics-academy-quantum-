from toolkit import *
UNIQUE = list(dict.fromkeys(ICON_NAMES))
FILES = {"learn": "learn", "lab": "lab", "games": "games", "bot": "ai_teacher", "settings": "settings", "user": "profile", "bell": "notifications", "search": "search",
         "video": "video", "file": "files", "note": "notes", "quiz": "quizzes", "points": "points", "level": "level", "trophy": "trophy", "award": "achievements",
         "calendar": "calendar", "download": "downloads", "volume": "sound", "mic": "microphone", "camera": "camera", "back": "back", "next": "next", "close": "close",
         "help": "help", "privacy": "privacy", "home": "home"}
def run():
    n = 0
    for g in UNIQUE:
        open(out("12_ICONS", f"{FILES[g]}.svg"), "w", encoding="utf-8").write(icon_svg(g)); n += 1
    open(out("12_ICONS", "progress.svg"), "w", encoding="utf-8").write(icon_svg("chart")); n += 1
    # preview sheet (for review only, not shipped)
    sheet = Image.new("RGB", (7 * 120, 4 * 120), (10, 16, 32)); art = Art(7 * 120, 4 * 120)
    for i, g in enumerate(UNIQUE): art.glyph(g, (i % 7) * 120 + 60, (i // 7) * 120 + 60, 64, C("#EAF2FF"), 2)
    sheet.paste(art.result(), (0, 0), art.result()); sheet.save("/tmp/icons_sheet.png"); return n
if __name__ == "__main__": print(run(), "icons")
