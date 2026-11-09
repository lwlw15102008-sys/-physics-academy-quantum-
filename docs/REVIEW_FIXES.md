# Review findings → fixes

| # | Finding | Fix |
|---|---|---|
| 1 | Android build blocker: no `gradle.properties` (`useAndroidX`) | Added `gradle.properties`, wrapper properties (jar/scripts must be generated: see Android README) |
| 2 | Android: no RTL support, no INTERNET permission | `supportsRtl=true`, INTERNET, forced RTL in Compose, debug-only cleartext manifest |
| 3 | CORS reflected any origin with credentials when `WEB_ORIGIN` unset | Explicit allow-list, wildcard rejected, https in prod, credentials off |
| 4 | No auth / validation / rate limit / helmet | Global JWT guard, roles, ValidationPipe, throttler, helmet, body limit |
| 5 | Prisma: no dependency, empty migration, `directUrl` missing | `prisma` dev-dep + scripts, `directUrl`, empty folder removed, README for generating migration |
| 6 | Schema: no FK indexes, no answer table, `isCorrect` leak risk, inconsistent status fields | Indexes, `QuizAnswer`, documented DTO rule, unified `ContentStatus`, CHECK constraints, RLS |
| 7 | Schema missing brief features (levels, tiers, competitions, daily challenge, streaks, labs, notes, notifications) | Models added + `seed/levels.json` (15 levels) |
| 8 | Web apps never called the API; admin had no auth | Student fetches catalogue with timeout/validation; admin middleware fails closed |
| 9 | Hard-coded date, version drift (0.1.0 / 0.2.0), fake notification dot, fake avatar | Client-side date, single version from `package.json`, honest empty states |
| 10 | Contrast 2.56:1 at 9–10px, no aria labels, no routing | Tokens (`--qa-dim` ≥ 4.5:1), min 11px, labels, real `Link` routes + `aria-current` |
| 11 | Concept art shipped in production UI; 3 copies of a 2.1 MB PNG | Removed from UI and duplicates deleted; WebP (236 KB) kept in assets |
| 12 | Runtime Google Fonts `@import` | `next/font` (self-hosted at build) |
| 13 | `getSubject` returned 200 for not-found; fabricated counts | 404 with error shape; counts removed |
| 14 | `@types/express@5` with Nest 10 | `^4.17.21` |
| 15 | `Menu` unused, `lint` without ESLint, unused `framer-motion`, unused shared dep, duplicated `.gitignore` | Cleaned; ESLint configs; `shared-types` now used |
| 16 | No tests / CI / lockfile / engines | API specs, GitHub Actions CI, `engines`, `.nvmrc` (lockfile needs a first local install) |
| 17 | Assets: 2 of ~103; 5 missing folders; logo unused; no transparent PNG | Folders created; logo, app icon, 3 backgrounds, 15 badges generated; logo/favicon wired into both apps |
| 18 | Android: `allowBackup="true"` في القالب | `allowBackup="false"` |
| 19 | الأصول: نقص كبير عن القائمة | 145/146 ملفاً بأسماء القائمة + مولّدات قابلة لإعادة التشغيل + مزامنة تلقائية للويب |
