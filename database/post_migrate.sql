-- Run once after `prisma migrate` (and again after later migrations; it is idempotent).
-- 1) Row Level Security: deny by default for every table in public.
-- 2) Revoke Supabase's anon/authenticated roles so the public anon key cannot read or write anything.
--    The API connects with the database owner role (bypasses RLS) and enforces authorization itself.
-- 3) Range constraints that Prisma cannot express.

DO $$
DECLARE r record;
BEGIN
  FOR r IN SELECT tablename FROM pg_tables WHERE schemaname = 'public' LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', r.tablename);
  END LOOP;

  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
    REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon;
    REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM anon;
    REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM anon;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM anon;
  END IF;
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
    REVOKE ALL ON ALL TABLES IN SCHEMA public FROM authenticated;
    REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM authenticated;
    REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM authenticated;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM authenticated;
  END IF;
END $$;

ALTER TABLE "LearningProgress" DROP CONSTRAINT IF EXISTS learning_progress_completion_range;
ALTER TABLE "LearningProgress" ADD CONSTRAINT learning_progress_completion_range CHECK ("completionRate" BETWEEN 0 AND 100);

ALTER TABLE "StudyPlan" DROP CONSTRAINT IF EXISTS study_plan_target_range;
ALTER TABLE "StudyPlan" ADD CONSTRAINT study_plan_target_range CHECK ("targetMinutes" BETWEEN 1 AND 1440);

ALTER TABLE "Quiz" DROP CONSTRAINT IF EXISTS quiz_time_limit_positive;
ALTER TABLE "Quiz" ADD CONSTRAINT quiz_time_limit_positive CHECK ("timeLimit" IS NULL OR "timeLimit" > 0);

ALTER TABLE "UserProfile" DROP CONSTRAINT IF EXISTS user_profile_counters_non_negative;
ALTER TABLE "UserProfile" ADD CONSTRAINT user_profile_counters_non_negative CHECK ("xp" >= 0 AND "currentStreak" >= 0 AND "longestStreak" >= 0);

ALTER TABLE "CompetitionEntry" DROP CONSTRAINT IF EXISTS competition_entry_score_non_negative;
ALTER TABLE "CompetitionEntry" ADD CONSTRAINT competition_entry_score_non_negative CHECK ("score" >= 0);

ALTER TABLE "Competition" DROP CONSTRAINT IF EXISTS competition_period_valid;
ALTER TABLE "Competition" ADD CONSTRAINT competition_period_valid CHECK ("endsAt" > "startsAt");

ALTER TABLE "Level" DROP CONSTRAINT IF EXISTS level_number_range;
ALTER TABLE "Level" ADD CONSTRAINT level_number_range CHECK ("number" BETWEEN 1 AND 15 AND "minXp" >= 0);
