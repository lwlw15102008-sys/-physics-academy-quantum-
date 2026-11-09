#!/usr/bin/env python3
"""Checks the asset brief (docx) file list against what exists and writes ASSET_MANIFEST.md."""
import os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
R = lambda sec, items: (sec, items)
LEVELS = ["silver", "gold", "platinum", "diamond", "elite", "star", "hero", "top", "expert", "innovator", "sage", "scholar", "genius", "master", "legend"]
SPEC = [
 ("01 البراند والخلفيات", [("01_BRANDING/logo/physics_academy_logo.png", "ok"), ("01_BRANDING/app_icon/app_icon.png", "ok")] + [(f"01_BRANDING/backgrounds/{n}.webp", "ok") for n in ("main_background", "auth_background", "learning_room")]),
 ("02 المدرس الذكي", [("02_AI_TEACHER/characters/teacher_main.png", "sub")] + [(f"02_AI_TEACHER/expressions/teacher_{n}.png", "sub") for n in ("happy", "explaining", "thinking", "pointing", "congratulations", "guidance", "listening")] + [("02_AI_TEACHER/avatars/teacher_avatar.png", "sub"), ("02_AI_TEACHER/avatars/teacher_profile.png", "sub")]),
 ("03 المواد", [(f"03_SUBJECTS/{d}/{n}_subject.webp", "ok") for d, n in (("physics", "physics"), ("chemistry", "chemistry"), ("biology", "biology"), ("mathematics", "math"), ("geology", "geology"))]),
 ("04 المختبرات", [(f"04_LABORATORIES/backgrounds/{n}_lab_bg.webp", "ok") for n in ("physics", "chemistry", "biology", "math", "geology")] + [("04_LABORATORIES/backgrounds/lab_table.png", "ok"), ("04_LABORATORIES/chemistry/test_tubes.png", "ok"), ("04_LABORATORIES/chemistry/lab_glassware.png", "ok"), ("04_LABORATORIES/physics/electrical_components.png", "ok"), ("04_LABORATORIES/physics/wires_batteries.png", "ok"), ("04_LABORATORIES/biology/microscope.png", "ok"), ("04_LABORATORIES/biology/cell_model.png", "ok"), ("04_LABORATORIES/biology/dna_model.png", "ok"), ("04_LABORATORIES/3d_models/human_body_model.glb", "no"), ("04_LABORATORIES/3d_models/molecules.glb", "ok"), ("04_LABORATORIES/3d_models/earth_models.glb", "ok")]),
 ("05 الألعاب", [(f"05_GAMES/covers/{n}.webp", "ok") for n in ("games_banner", "daily_challenge", "science_puzzle", "physics_challenge", "chemistry_challenge", "biology_challenge", "time_challenge", "experiment_game")] + [(f"05_GAMES/objects/{n}.png", "ok") for n in ("mystery_box", "game_victory", "game_retry")]),
 ("06 المستويات والمكافآت", [(f"06_REWARDS/levels/level_{i + 1:02d}_{s}.png", "ok") for i, s in enumerate(LEVELS)] + [(f"06_REWARDS/badges/{n}.png", "ok") for n in ("badge_physics_genius", "badge_chemistry_scientist", "badge_biology_expert", "badge_first_lesson", "badge_first_unit", "badge_100_problems", "badge_concept_mastery", "badge_experiment_complete", "badge_learning_streak", "badge_daily_challenge", "badge_quiz_excellence", "badge_regular_review")] + [(f"06_REWARDS/trophies/trophy_rank_{i}.png", "ok") for i in range(1, 6)]),
 ("07 المسابقات", [("07_COMPETITIONS/competition_banner.webp", "ok"), ("07_COMPETITIONS/leaderboard_background.webp", "ok"), ("07_COMPETITIONS/podium_first.png", "ok"), ("07_COMPETITIONS/podium_second.png", "ok"), ("07_COMPETITIONS/podium_third.png", "ok"), ("07_COMPETITIONS/competition_medal.png", "ok"), ("07_COMPETITIONS/winner_celebration.png", "ok")]),
 ("08 الواجهة", [(f"08_UI_ILLUSTRATIONS/{n}.webp", "ok") for n in ("onboarding_01", "onboarding_02", "onboarding_03", "onboarding_04", "welcome_illustration", "empty_courses", "empty_downloads", "empty_notifications", "no_internet", "error_illustration", "success_illustration", "loading_illustration")] + [("08_UI_ILLUSTRATIONS/student_profile_default.png", "ok")]),
 ("09 المذاكرة والتقارير", [(f"09_STUDY_ANALYTICS/{n}.webp", "ok") for n in ("study_planner", "weekly_report", "learning_progress", "student_analytics", "study_calendar", "digital_notebook", "revision_mode", "focus_mode")]),
 ("10 الاشتراكات", [(f"10_SUBSCRIPTIONS/{n}", "ok") for n in ("plan_free.png", "plan_pro.png", "plan_vip.png", "subscription_banner.webp", "premium_features.webp")]),
 ("11 الموقع", [(f"11_WEBSITE/{n}.webp", "ok") for n in ("website_hero", "website_features", "website_labs", "website_ai_teacher", "admin_dashboard_bg", "teacher_dashboard_bg")]),
 ("12 الأيقونات (SVG)", [(f"12_ICONS/{n}.svg", "ok") for n in ("home", "learn", "lab", "games", "progress", "ai_teacher", "settings", "profile", "notifications", "search", "video", "files", "notes", "quizzes", "points", "level", "trophy", "achievements", "calendar", "downloads", "sound", "microphone", "camera", "back", "next", "close", "help", "privacy")]),
]
NOTE = {"sub": "بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية)", "ok": "مولَّد برمجياً", "no": "غير متاح — يحتاج نموذج تشريح حقيقي"}
def main():
    tot = got = 0; lines = []
    for sec, items in SPEC:
        lines += [f"### {sec}", "", "| الملف | الحالة |", "|---|---|"]; s_got = 0
        for path, kind in items:
            exists = os.path.exists(os.path.join(ROOT, path)); tot += 1; got += exists; s_got += exists
            lines.append(f"| `{path}` | {'✅ ' + NOTE[kind] if exists else '❌ ' + NOTE.get(kind, 'مفقود') if kind == 'no' else ('✅ ' + NOTE[kind]) if exists else '❌ مفقود'} |")
        lines += ["", f"**{s_got}/{len(items)}**", ""]
    head = ["# Asset Manifest (v0.4.0)", "", f"الحالة الفعلية مقابل أسماء قائمة الأصول: **{got} من {tot}** ملفاً موجوداً.", "",
            "كل الأصول **مولّدة برمجياً** (PIL + numpy) من `tools/generate_all.py`، وهي رسومات مسطّحة/شبه ثلاثية الأبعاد بهوية موحّدة. ليست رندرات 3D احترافية ولا صوراً فوتوغرافية.",
            "", "## ما لا يمكن توليده بهذه الطريقة", "",
            "- `human_body_model.glb`: نموذج تشريح بشري حقيقي (يحتاج نموذجاً مرخّصاً أو فناناً ثلاثي الأبعاد).",
            "- مدرس ثلاثي الأبعاد متحرك (GLB): المسلَّم روبوت 2D بنفس الشخصية في كل الصور.",
            "- 05_GAMES/characters، وصور وحدات/فصول/دروس كل مادة (قوالب موحّدة تُولَّد لاحقاً حسب المحتوى).",
            "- جودة الرندر السينمائي في الشارات والكؤوس: لو أردتها فاستخدم `PROMPTS_FOR_AI_IMAGE_TOOLS.md` لتوليدها بأداة صور.",
            "", "## تفصيل الملفات", ""]
    open(os.path.join(ROOT, "ASSET_MANIFEST.md"), "w", encoding="utf-8").write("\n".join(head + lines) + "\n"); print(f"{got}/{tot}")
main()
