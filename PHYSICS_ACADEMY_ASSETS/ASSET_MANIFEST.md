# Asset Manifest (v0.4.0)

الحالة الفعلية مقابل أسماء قائمة الأصول: **145 من 146** ملفاً موجوداً.

كل الأصول **مولّدة برمجياً** (PIL + numpy) من `tools/generate_all.py`، وهي رسومات مسطّحة/شبه ثلاثية الأبعاد بهوية موحّدة. ليست رندرات 3D احترافية ولا صوراً فوتوغرافية.

## ما لا يمكن توليده بهذه الطريقة

- `human_body_model.glb`: نموذج تشريح بشري حقيقي (يحتاج نموذجاً مرخّصاً أو فناناً ثلاثي الأبعاد).
- مدرس ثلاثي الأبعاد متحرك (GLB): المسلَّم روبوت 2D بنفس الشخصية في كل الصور.
- 05_GAMES/characters، وصور وحدات/فصول/دروس كل مادة (قوالب موحّدة تُولَّد لاحقاً حسب المحتوى).
- جودة الرندر السينمائي في الشارات والكؤوس: لو أردتها فاستخدم `PROMPTS_FOR_AI_IMAGE_TOOLS.md` لتوليدها بأداة صور.

## تفصيل الملفات

### 01 البراند والخلفيات

| الملف | الحالة |
|---|---|
| `01_BRANDING/logo/physics_academy_logo.png` | ✅ مولَّد برمجياً |
| `01_BRANDING/app_icon/app_icon.png` | ✅ مولَّد برمجياً |
| `01_BRANDING/backgrounds/main_background.webp` | ✅ مولَّد برمجياً |
| `01_BRANDING/backgrounds/auth_background.webp` | ✅ مولَّد برمجياً |
| `01_BRANDING/backgrounds/learning_room.webp` | ✅ مولَّد برمجياً |

**5/5**

### 02 المدرس الذكي

| الملف | الحالة |
|---|---|
| `02_AI_TEACHER/characters/teacher_main.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/expressions/teacher_happy.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/expressions/teacher_explaining.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/expressions/teacher_thinking.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/expressions/teacher_pointing.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/expressions/teacher_congratulations.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/expressions/teacher_guidance.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/expressions/teacher_listening.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/avatars/teacher_avatar.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |
| `02_AI_TEACHER/avatars/teacher_profile.png` | ✅ بديل: روبوت معلّم ثنائي الأبعاد (ليس شخصية 3D بشرية) |

**10/10**

### 03 المواد

| الملف | الحالة |
|---|---|
| `03_SUBJECTS/physics/physics_subject.webp` | ✅ مولَّد برمجياً |
| `03_SUBJECTS/chemistry/chemistry_subject.webp` | ✅ مولَّد برمجياً |
| `03_SUBJECTS/biology/biology_subject.webp` | ✅ مولَّد برمجياً |
| `03_SUBJECTS/mathematics/math_subject.webp` | ✅ مولَّد برمجياً |
| `03_SUBJECTS/geology/geology_subject.webp` | ✅ مولَّد برمجياً |

**5/5**

### 04 المختبرات

| الملف | الحالة |
|---|---|
| `04_LABORATORIES/backgrounds/physics_lab_bg.webp` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/backgrounds/chemistry_lab_bg.webp` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/backgrounds/biology_lab_bg.webp` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/backgrounds/math_lab_bg.webp` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/backgrounds/geology_lab_bg.webp` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/backgrounds/lab_table.png` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/chemistry/test_tubes.png` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/chemistry/lab_glassware.png` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/physics/electrical_components.png` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/physics/wires_batteries.png` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/biology/microscope.png` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/biology/cell_model.png` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/biology/dna_model.png` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/3d_models/human_body_model.glb` | ❌ غير متاح — يحتاج نموذج تشريح حقيقي |
| `04_LABORATORIES/3d_models/molecules.glb` | ✅ مولَّد برمجياً |
| `04_LABORATORIES/3d_models/earth_models.glb` | ✅ مولَّد برمجياً |

**15/16**

### 05 الألعاب

| الملف | الحالة |
|---|---|
| `05_GAMES/covers/games_banner.webp` | ✅ مولَّد برمجياً |
| `05_GAMES/covers/daily_challenge.webp` | ✅ مولَّد برمجياً |
| `05_GAMES/covers/science_puzzle.webp` | ✅ مولَّد برمجياً |
| `05_GAMES/covers/physics_challenge.webp` | ✅ مولَّد برمجياً |
| `05_GAMES/covers/chemistry_challenge.webp` | ✅ مولَّد برمجياً |
| `05_GAMES/covers/biology_challenge.webp` | ✅ مولَّد برمجياً |
| `05_GAMES/covers/time_challenge.webp` | ✅ مولَّد برمجياً |
| `05_GAMES/covers/experiment_game.webp` | ✅ مولَّد برمجياً |
| `05_GAMES/objects/mystery_box.png` | ✅ مولَّد برمجياً |
| `05_GAMES/objects/game_victory.png` | ✅ مولَّد برمجياً |
| `05_GAMES/objects/game_retry.png` | ✅ مولَّد برمجياً |

**11/11**

### 06 المستويات والمكافآت

| الملف | الحالة |
|---|---|
| `06_REWARDS/levels/level_01_silver.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_02_gold.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_03_platinum.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_04_diamond.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_05_elite.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_06_star.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_07_hero.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_08_top.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_09_expert.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_10_innovator.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_11_sage.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_12_scholar.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_13_genius.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_14_master.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/levels/level_15_legend.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_physics_genius.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_chemistry_scientist.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_biology_expert.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_first_lesson.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_first_unit.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_100_problems.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_concept_mastery.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_experiment_complete.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_learning_streak.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_daily_challenge.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_quiz_excellence.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/badges/badge_regular_review.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/trophies/trophy_rank_1.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/trophies/trophy_rank_2.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/trophies/trophy_rank_3.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/trophies/trophy_rank_4.png` | ✅ مولَّد برمجياً |
| `06_REWARDS/trophies/trophy_rank_5.png` | ✅ مولَّد برمجياً |

**32/32**

### 07 المسابقات

| الملف | الحالة |
|---|---|
| `07_COMPETITIONS/competition_banner.webp` | ✅ مولَّد برمجياً |
| `07_COMPETITIONS/leaderboard_background.webp` | ✅ مولَّد برمجياً |
| `07_COMPETITIONS/podium_first.png` | ✅ مولَّد برمجياً |
| `07_COMPETITIONS/podium_second.png` | ✅ مولَّد برمجياً |
| `07_COMPETITIONS/podium_third.png` | ✅ مولَّد برمجياً |
| `07_COMPETITIONS/competition_medal.png` | ✅ مولَّد برمجياً |
| `07_COMPETITIONS/winner_celebration.png` | ✅ مولَّد برمجياً |

**7/7**

### 08 الواجهة

| الملف | الحالة |
|---|---|
| `08_UI_ILLUSTRATIONS/onboarding_01.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/onboarding_02.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/onboarding_03.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/onboarding_04.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/welcome_illustration.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/empty_courses.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/empty_downloads.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/empty_notifications.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/no_internet.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/error_illustration.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/success_illustration.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/loading_illustration.webp` | ✅ مولَّد برمجياً |
| `08_UI_ILLUSTRATIONS/student_profile_default.png` | ✅ مولَّد برمجياً |

**13/13**

### 09 المذاكرة والتقارير

| الملف | الحالة |
|---|---|
| `09_STUDY_ANALYTICS/study_planner.webp` | ✅ مولَّد برمجياً |
| `09_STUDY_ANALYTICS/weekly_report.webp` | ✅ مولَّد برمجياً |
| `09_STUDY_ANALYTICS/learning_progress.webp` | ✅ مولَّد برمجياً |
| `09_STUDY_ANALYTICS/student_analytics.webp` | ✅ مولَّد برمجياً |
| `09_STUDY_ANALYTICS/study_calendar.webp` | ✅ مولَّد برمجياً |
| `09_STUDY_ANALYTICS/digital_notebook.webp` | ✅ مولَّد برمجياً |
| `09_STUDY_ANALYTICS/revision_mode.webp` | ✅ مولَّد برمجياً |
| `09_STUDY_ANALYTICS/focus_mode.webp` | ✅ مولَّد برمجياً |

**8/8**

### 10 الاشتراكات

| الملف | الحالة |
|---|---|
| `10_SUBSCRIPTIONS/plan_free.png` | ✅ مولَّد برمجياً |
| `10_SUBSCRIPTIONS/plan_pro.png` | ✅ مولَّد برمجياً |
| `10_SUBSCRIPTIONS/plan_vip.png` | ✅ مولَّد برمجياً |
| `10_SUBSCRIPTIONS/subscription_banner.webp` | ✅ مولَّد برمجياً |
| `10_SUBSCRIPTIONS/premium_features.webp` | ✅ مولَّد برمجياً |

**5/5**

### 11 الموقع

| الملف | الحالة |
|---|---|
| `11_WEBSITE/website_hero.webp` | ✅ مولَّد برمجياً |
| `11_WEBSITE/website_features.webp` | ✅ مولَّد برمجياً |
| `11_WEBSITE/website_labs.webp` | ✅ مولَّد برمجياً |
| `11_WEBSITE/website_ai_teacher.webp` | ✅ مولَّد برمجياً |
| `11_WEBSITE/admin_dashboard_bg.webp` | ✅ مولَّد برمجياً |
| `11_WEBSITE/teacher_dashboard_bg.webp` | ✅ مولَّد برمجياً |

**6/6**

### 12 الأيقونات (SVG)

| الملف | الحالة |
|---|---|
| `12_ICONS/home.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/learn.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/lab.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/games.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/progress.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/ai_teacher.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/settings.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/profile.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/notifications.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/search.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/video.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/files.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/notes.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/quizzes.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/points.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/level.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/trophy.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/achievements.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/calendar.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/downloads.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/sound.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/microphone.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/camera.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/back.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/next.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/close.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/help.svg` | ✅ مولَّد برمجياً |
| `12_ICONS/privacy.svg` | ✅ مولَّد برمجياً |

**28/28**

