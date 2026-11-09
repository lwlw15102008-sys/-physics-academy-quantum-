# Security notes (v0.3.0)

## Implemented
- **CORS**: explicit allow-list only (`WEB_ORIGIN`); `*`/`null` rejected at startup; https required in production; `credentials:false` (bearer tokens, no cookies → no CSRF surface).
- **Auth (API)**: global default-deny `AuthGuard`; HS256 JWT verified with constant-time compare, `alg` pinned, `exp` mandatory, `aud`/`iss` checked; missing secret → 503 (fail closed). Role is read from `app_metadata` only (`user_metadata` is user-editable) and unknown roles collapse to `STUDENT`. `RolesGuard` + `@Roles()` for admin-only routes.
- **Startup validation**: production refuses to boot without https `WEB_ORIGIN` and a ≥32-char `SUPABASE_JWT_SECRET`.
- **Hardening**: `helmet`, 100 kB body limit, global rate limit (`@nestjs/throttler`), `ValidationPipe` (whitelist + forbidNonWhitelisted), slug whitelist validation.
- **Errors**: one shape `{ error: { code, message, requestId } }`; 5xx never leak internals; `x-request-id` sanitised.
- **Caching**: per-user responses `no-store`; admin responses `no-store` + `noindex`.
- **Admin web**: middleware denies every route without a valid admin/owner JWT cookie (`pa_session`) in production; per-request **nonce CSP** with `strict-dynamic`; `/login` is the only open path.
- **Student web**: security headers (HSTS, `X-Frame-Options: DENY`, `nosniff`, referrer/permissions policy, CSP). Error boundary never prints error details.
- **Database**: RLS enabled on every table, `anon`/`authenticated` revoked (`database/post_migrate.sql`), CHECK constraints, FK indexes, server-side grading table.
- **Android**: HTTPS only in release, `allowBackup=false`, R8 on.
- **Secrets**: none in the repo; `.env*` ignored; service-role and AI keys are server-only.

## Known limits / to do before launch
1. **No login flow yet.** Admin and protected API routes are locked until Supabase Auth is wired and a session cookie (`pa_session`) / bearer token is issued.
2. Student-web CSP still allows inline scripts (`'unsafe-inline'`) because Next 14 static pages emit inline bootstrap scripts. Move to nonce CSP if user-generated content is ever rendered.
3. Run `npm install` then `npm audit` and commit `package-lock.json`; keep Next.js on the latest 14.2.x patch.
4. Rate limiting is per-process memory; use a shared store (Redis) when running several API instances.
5. Quiz endpoints must never select `QuizOption.isCorrect` for students; compute XP/scores server-side only.
6. AI tutor: call the provider from the API only, with per-user limits and prompt-injection review.
7. Add logging/monitoring, backups, and a dependency-update bot.
