# PHYSICS ACADEMY | QUANTUM LEARNING UNIVERSE — v0.4.0

منصة تعليمية عربية (RTL): واجهة طالب، لوحة إدارة، API، قاعدة بيانات، وتطبيق Android.
**الحالة: هيكل تأسيسي محسَّن أمنياً — ليس منصة جاهزة للإطلاق.** راجع `docs/IMPLEMENTATION_STATUS.md`.

## التشغيل المحلي
```bash
cp .env.example .env          # عدّل القيم (SUPABASE_JWT_SECRET ≥ 32 حرفاً لتفعيل المسارات المحمية)
npm install                   # ثم احفظ package-lock.json في المستودع
npm run dev:api               # http://localhost:4000/api/v1/health
npm run dev:web               # http://localhost:3000
npm run dev:admin             # http://localhost:3001
npm run lint && npm run typecheck && npm test && npm run build
```
قاعدة البيانات: `database/README.md`. Android: `apps/android-cogo/README.md`.
الأصول البصرية: `python3 PHYSICS_ACADEMY_ASSETS/tools/generate_all.py` يعيد توليدها كلها، و`npm run assets:sync` ينسخ المطلوب إلى تطبيقَي الويب (يعمل تلقائياً قبل `dev` و`build`). قائمتها الفعلية في `PHYSICS_ACADEMY_ASSETS/ASSET_MANIFEST.md`.

## البنية
| المسار | المحتوى |
|---|---|
| `apps/student-web` | Next.js — واجهة الطالب (مسارات: `/` `/learn` `/labs` `/games` `/progress`) |
| `apps/admin-web` | Next.js — لوحة الإدارة، محجوبة بالمصادقة في الإنتاج |
| `apps/android-cogo` | **تطبيق Android المعتمد** (Java + Material 3 + ViewBinding، RTL) — يُبنى في Code on the Go، بدون مفاتيح توقيع |
| `apps/android` | هيكل Kotlin/Compose قديم لم يُبنَ — مُستبدَل بـ `android-cogo` |
| `services/api` | NestJS — مصادقة JWT، أدوار، تحديد معدل، تحقق مدخلات |
| `database` | مخطط Prisma + `post_migrate.sql` (RLS وقيود) + بذور المستويات |
| `packages/*` | `shared-types`, `design-tokens`, `web-config` (ترويسات الأمان) |

## الأمان — ملخص
انظر `docs/SECURITY.md`. أهم القواعد: CORS بقائمة صريحة، المصادقة مفروضة افتراضياً على كل مسار (`@Public()` للاستثناء)، رفض أي إعداد إنتاج غير آمن عند الإقلاع، RLS مفعّل بالرفض الافتراضي، وأسرار الخادم لا تُكشف للمتصفح.


## Authentication policy

The current product requirement is Google-only sign-in (no manual account creation or password login). See [`docs/GOOGLE_ONLY_AUTH.md`](docs/GOOGLE_ONLY_AUTH.md) for implementation boundaries and the required Supabase/Google setup. Native Android Google sign-in remains pending.
