# Implementation status — v0.4.0

| Area | Status |
|---|---|
| Assets | **145 من 146 ملفاً** بأسماء قائمة الأصول (مولّدة برمجياً): هوية، 3 خلفيات، روبوت معلّم بـ8 تعبيرات، 5 مواد، 5 مختبرات + 8 أدوات، 8 ألعاب، 15 مستوى + 12 شارة + 5 كؤوس + 3 ميداليات، مسابقات، واجهة، تحليلات، باقات، موقع، 28 أيقونة SVG، 3 نماذج GLB. **الناقص:** جسم الإنسان 3D. الجودة مسطّحة/شبه 3D وليست رندر سينمائي (راجع `PROMPTS_FOR_AI_IMAGE_TOOLS.md`). |
| Student web | مسارات حقيقية + صور المواد والمختبرات والألعاب وسلّم المستويات والمدرس. المحتوى التعليمي نفسه ما زال Placeholder. |
| Admin web | مسارات + حجب بالمصادقة + CSP بـ nonce. لا تسجيل دخول ولا بيانات. |
| API | هيكل محصّن (JWT، أدوار، تحديد معدل). بيانات تجريبية بلا قاعدة بيانات. |
| Database | مخطط كامل (23 نموذجاً) + RLS/قيود. لم يُولَّد migration ولا بذور. |
| Android | `apps/android-cogo` على قالب Code on the Go: 5 تبويبات بصور. لم يُبنَ في بيئة المراجعة. |
| 3D / Games / AI tutor | نماذج GLB جاهزة للعرض؛ **لا يوجد عارض ثلاثي الأبعاد ولا منطق ألعاب ولا ذكاء اصطناعي بعد.** |
| Tests | وحدات API (JWT، إعدادات، حراس، كتالوج). لا اختبارات للويب أو Android. |

## ما نُفِّذ فعلاً في بيئة المراجعة
اختبارات JWT والإعدادات (11) ومحقق JWT للإدارة (11) ومنطق ترويسات الأمان، وفحص صياغة TS/TSX وJava، وتطابق الموارد وحقول ViewBinding في Android، وتحقق بنيوي من ملفات GLB (الرؤوس والفهارس والحدود).
## لم يُنفَّذ (لا شبكة ولا SDK)
`npm install/build/lint`, `jest`, `prisma migrate`, بناء Android. جرّبها عندك وابعث أي خطأ.


## Build iteration — 2026-11-09: learning progression rules
- Added `services/api/src/modules/learning/learning-policy.ts` as a pure server-side domain policy for video completion, lesson gates, admin lock/unlock precedence, and final-exam eligibility.
- Defaults: 90% video completion; final exam requires at least 50 questions and 50% correct. Both thresholds are configurable through a policy argument so the future owner settings can supply persisted values.
- Added `learning-policy.spec.ts` with 11 Jest cases covering thresholds, invalid inputs, admin overrides, and exam eligibility.
- Validation performed in this workspace: strict TypeScript compilation passed; 7 direct Node runtime assertions passed.
- Not yet connected: Prisma persistence, authenticated API endpoints, trusted playback-heartbeat ingestion, admin UI controls, and actual exam/question delivery. The policy module alone does not enforce these until integrated with those layers.


## Build iteration — 2026-11-09: playback heartbeat validation
- Added `video-heartbeat.ts`: a pure server-side policy for deriving credited watch time from heartbeat intervals rather than trusting a client-supplied watched-seconds total.
- Rejects invalid media positions, duration changes, heartbeat spam, stale heartbeat gaps, and implausible forward/backward seeking.
- Credits at most 15 seconds per heartbeat and caps credited time at media duration.
- Added 9 Jest cases covering accepted playback and abuse/edge cases.
- Important integration boundary: this is the validation/domain layer only. It must be called by an authenticated API endpoint and persisted atomically per user+lesson before it can enforce playback in production. It does not yet authenticate the media asset or prove that a human is watching.


## Google-only authentication update (v0.4.3)
- Student web: Google OAuth/PKCE login screen, callback exchange, and client-side session gate added.
- Admin web: Google OAuth/PKCE login and trusted `app_metadata.role` gate added; existing middleware continues to enforce ADMIN/OWNER JWT roles.
- Supabase SQL trigger added to create the student profile automatically on first OAuth identity creation.
- No manual registration/password login UI is provided.
- External Google/Supabase credentials and provider configuration are still required; no live OAuth test was possible in this workspace.
- Native Android Google sign-in is not yet implemented.
