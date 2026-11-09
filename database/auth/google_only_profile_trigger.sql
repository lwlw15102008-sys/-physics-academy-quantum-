-- PHYSICS ACADEMY: create the app profile automatically after the first
-- successful Google OAuth sign-in. No public/manual sign-up endpoint is needed.
-- Run in the Supabase SQL Editor after reviewing the project schema.

create or replace function public.handle_new_auth_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public."UserProfile" ("authUserId", "displayName", "role", "updatedAt")
  values (
    new.id::text,
    coalesce(nullif(new.raw_user_meta_data ->> 'full_name', ''),
             nullif(new.raw_user_meta_data ->> 'name', ''),
             split_part(coalesce(new.email, 'طالب'), '@', 1)),
    'STUDENT'::public."UserRole",
    now()
  )
  on conflict ("authUserId") do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created_profile on auth.users;
create trigger on_auth_user_created_profile
after insert on auth.users
for each row execute procedure public.handle_new_auth_user();

-- IMPORTANT: grant ADMIN/OWNER only through a trusted server/admin process.
-- Never derive privileged roles from Google profile metadata supplied by users.
