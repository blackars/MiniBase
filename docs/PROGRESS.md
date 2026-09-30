# MiniBase Web — progreso

## Stack congelado
Next.js 14 + FastAPI + Supabase (Auth+RLS+pgvector) + Cloudinary primario + R2/Drive backup.

## Checklist P1-P3 (hoy)
- [x] Rama `minibase-web`
- [x] `00_SYSTEM_PROMPT.md` (pack anti-pérdida)
- [x] `supabase/migrations/001_init.sql` (modelo futuro-proof + RLS + vector)
- [x] `api/main.py + routers/minis,imports,agent,table + scripts/migrate_sqlite.py`
- [x] `web/app/page.tsx` oscuro + detalle + lib/supabase
- [ ] Poner credenciales en `web/.env` + `api/.env` (SUPABASE_URL, CLOUDINARY_*, R2_*)
- [ ] `supabase db push` + `pip install -r api/requirements.txt && uvicorn main:app --reload` + `npm i --prefix web && npm run dev --prefix web`
- [ ] Importar `template.xlsx` vía `/api/imports/excel/preview` y migrar `src/miniatures.db` con `python api/scripts/migrate_sqlite.py src/miniatures.db`
- [ ] Siguiente: PROMPT_04_CV_DATASET, PROMPT_05_TABLE_STATE

## Consideraciones gratuitas + seguridad
- Costo 0: Supabase Free 500MB, Vercel Hobby, Render/Fly free, Cloudinary free, R2 10GB free.
- Fotos: `signed upload`, `public_id=minibase/{user}/{collection}/{slug}/{view}`, `eager 800+200`, backup async a R2 + `pg_dump` a Drive.
- Auth: Google OAuth, RLS por colección, scope Drive `drive.file` solo.
- CV/tablero: `images.phash + miniatures.embedding` para webcam; `/api/table/state` con `grid_visible=true` solo si `phase=movement`.
