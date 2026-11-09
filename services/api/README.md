# API service

NestJS service. Run `npm --workspace services/api run start:dev`.

- `GET /api/v1/health` — service status.
- `GET /api/v1/catalog/subjects` — demo catalogue (not persisted).
- `GET /api/v1/catalog/subjects/:slug` — demo subject details.
- `GET /api/v1/catalog/learning-path` — placeholder student learning path.

Database and auth are intentionally not wired until Supabase authorization and environment secrets are configured.
