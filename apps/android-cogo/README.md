# Physics Academy — Android (Code on the Go)

مشروع Java + Material 3 + ViewBinding مبني على قالب Code on the Go، واجهة عربية RTL مفروضة، يعمل **بدون إنترنت**.

## الشاشات الحالية
- الرئيسية، تعلّم (المواد الخمس بصورها)، المختبرات (5)، الألعاب (7)، تقدّمي (سلّم 15 مستوى بشاراته).
- لا توجد بيانات تقدّم حقيقية بعد؛ الإحصاءات "—" عمداً.

## الفتح والبناء
1. انسخ هذا المجلد إلى `/storage/emulated/0/CodeOnTheGoProjects/` وافتحه من Code on the Go ثم Build.
2. لم تُغيَّر ملفات البناء (`build.gradle.kts`, `libs.versions.toml`) عن القالب عمداً.

## ملاحظات
- `applicationId` ما زال `com.example.physicsacademy` من القالب؛ غيّره قبل النشر.
- `allowBackup=false`. مفاتيح التوقيع (`release.keystore`/`release.properties`) غير مضمّنة ومُدرجة في `.gitignore`؛ ولّد مفتاحاً جديداً قبل أي نشر.
- الصور في `res/drawable-nodpi` مصغّرة من `PHYSICS_ACADEMY_ASSETS`.
- لم يُنفَّذ البناء في بيئة المراجعة (لا Android SDK).
