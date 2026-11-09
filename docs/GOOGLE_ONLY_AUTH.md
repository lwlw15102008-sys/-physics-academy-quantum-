# Google-only authentication (v0.4.3)

## Product rule
- Google OAuth is the only sign-in method exposed in the student and admin web clients.
- There is no manual registration form, email/password login, or password-reset flow.
- Supabase Auth creates its auth identity on the first successful Google sign-in. The SQL trigger in `database/auth/google_only_profile_trigger.sql` creates the matching `UserProfile` with the `STUDENT` role exactly once.
- Admin access is separate from student registration: only accounts whose trusted Supabase `app_metadata.role` is `ADMIN` or `OWNER` can enter the admin console. A Google account alone never grants a privileged role.

## Required external setup (not included in the ZIP)
1. Create/configure a Supabase project and set `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` in both web app environments.
2. In Supabase Authentication → Providers, enable Google and configure the Google OAuth Client ID and Secret.
3. In Google Cloud Console, add the Supabase callback URL shown by Supabase (usually `https://<project-ref>.supabase.co/auth/v1/callback`) to the OAuth client's authorized redirect URIs.
4. In Supabase Authentication → URL Configuration, allow the exact app callback URLs: `http://localhost:3000/auth/callback`, `http://localhost:3001/auth/callback`, and the production HTTPS callback URLs for each deployed app.
5. Disable Email provider/password sign-in and any other providers in Supabase if the project is intended to enforce Google-only authentication globally.
6. Run `database/auth/google_only_profile_trigger.sql` in the Supabase SQL Editor after the Prisma schema has been migrated.
7. For the admin web app, configure `SUPABASE_JWT_SECRET` with the project's compatible HS256 JWT secret because the existing admin middleware verifies HS256 tokens. Confirm the Supabase project is issuing HS256 JWTs before enabling production admin login; projects using asymmetric signing keys need a JWKS-based verifier instead.
8. Grant admin roles only through a trusted server-side Supabase Admin API process by setting `app_metadata.role` to `ADMIN` or `OWNER`. Never set privileged roles from editable `user_metadata` or from the browser.

## Current implementation boundary
- Student web: Google OAuth start, PKCE callback exchange, session check on the student route group, and login-only entry screen are implemented in source.
- Admin web: Google OAuth start and callback are implemented; the callback requires trusted `app_metadata.role`, then writes the access token to the existing `pa_session` cookie consumed by the admin middleware. This cookie is JavaScript-readable; production hardening should move session establishment to a server-side HttpOnly cookie endpoint.
- Android: native Google sign-in is **not yet implemented** in either Android project. Do not treat this web change as proof that the APK uses Google-only login.
- No live Google/Supabase credentials were supplied, so OAuth could not be exercised against a real provider from this workspace. Configure provider credentials and redirect URLs before deployment.

## Verification checklist
- First Google sign-in creates one `auth.users` record and one `UserProfile` with role `STUDENT`.
- Subsequent sign-ins reuse the same identity/profile; trigger uses `ON CONFLICT DO NOTHING`.
- Student routes redirect to `/login` without a valid Supabase session.
- Admin callback rejects users without trusted `app_metadata.role` of `ADMIN` or `OWNER`.
- Test callback URLs, token expiry/refresh, logout, and role revocation on the deployed domains before production.
