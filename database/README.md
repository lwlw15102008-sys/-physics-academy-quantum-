# Database

1. Copy `.env.example` to `.env` and set `DATABASE_URL` (pooled) and `DIRECT_URL` (direct, used by migrations).
2. `npm --workspace services/api run db:migrate -- --name init` — generates `migrations/` from `schema.prisma`.
3. Apply `post_migrate.sql` (Supabase SQL editor or `psql`): enables RLS deny-by-default, revokes `anon`/`authenticated`, adds CHECK constraints. Re-run after every migration.
4. Load `seed/levels.json` into `Level` (a seed script is not included yet).

Rules the API must follow: never select `QuizOption.isCorrect` for students; compute `xp`, quiz scores and competition scores on the server only; accept `Lesson.sourceUrl` as https only.
