# MiniBase Web — System Prompt Pack (rama `minibase-web`)

> Archivo de recuperación de contexto. Cuando pierdas contexto en sesiones futuras,
> el usuario te pegará uno de los PROMPTS de abajo. Lee este archivo primero + el
> archivo del módulo indicado. No reinventes el stack.

## 0. Contexto inmutable

* **Origen:** app desktop Python Tkinter + SQLite (`src/schema.sql`, `src/creation_module.py`,
  `src/importation_module.py`, `src/photo_uploader.py`). Bug conocido:
  `creation_module.py:152` hace `(name[0])` en vez de `(name,)` — inserta solo 1ª letra.
* **Objetivo final:** inventario real de miniaturas que alimenta a IA agéntica:
  DM que narra con inventario real, CV que reconoce minis por webcam en tablero,
  proyector que dibuja escenarios/animaciones/grid solo en fase de movimiento.
* **Stack congelado (gratuito):** `Next.js 14 App Router + TS + Tailwind + shadcn/ui dark`
  en Vercel + `FastAPI + SQLAlchemy + Pydantic + Pandas/OpenPyXL` en Render/Fly +
  `Supabase Postgres + Auth Google + RLS + pgvector` + `Cloudinary (primario)` +
  `Cloudflare R2 / Drive (backup)`.
* **Estética:** oscura moderna, nada Tkinter. Cada colección exige Auth.
* **Rama:** todo el web port vive en `minibase-web` desprendida de `master`.
  Estructura: `/web` `/api` `/supabase/migrations` `/prompts` `/docs`.

## 1. Modelo de datos canónico (ver `supabase/migrations/001_init.sql`)

`users > collections > miniatures (+type: mini|scenery|token|tile|prop, quantity, slug,
completeness_score, embedding vector(512)) > visual_metadata > images
(cloudinary_public_id, secure_url, backup_url, phash, w/h) > tags + miniature_tags >
lore > rpg_profile(stats JSONB, movement, range) > gameplay_usage > imports > missing_fields >
surveys > agent_tasks > table_state`.

Reglas: RLS por `auth.uid()=user_id`, Cloudinary path
`minibase/{user}/{collection}/{slug}/{view_type}`, 13 vistas canónicas
(frontal, black_background, white_background, lateral_1/2, back, top, bottom,
close_up, isometric, model_3d, video_gif, other).

## 2. Contratos API (ver `api/main.py`)

* `GET /api/minis?q=&tag=&type=&collection_id=` — lista + filtros + completeness
* `POST /api/minis` `PATCH /api/minis/{id}` `DELETE /api/minis/{id}`
* `POST /api/minis/{id}/images/sign` — firma Cloudinary, devuelve `public_id` esperado
* `POST /api/imports/excel` — xlsx/csv → preview columnas → mapping → upsert
* `GET /api/agent/search?query=` — búsqueda semántica pgvector + filtros
* `GET /api/table/state?collection_id=` — `{phase, grid_visible, tokens:[{mini_id,x,y}]}` para proyector
* `POST /api/table/state` — el DM actualiza fase; si `phase=movement` → `grid_visible=true`
* Todo con `OpenAPI.json` para MCP: tools `list_miniatures, search_semantic, get_dataset, spawn_scenario`.

## 3. Seguridad / fotos

* Supabase Auth Google, scope Drive `drive.file` únicamente.
* Cloudinary `signed upload preset`, `eager 800px+200px thumb`, strip EXIF.
* Backup async FastAPI cron: Cloudinary → R2 (`backup_url`) + `pg_dump` semanal → Drive.
* Nunca commitear `.env`. Ver `web/.env.example`, `api/.env.example`.

## 4. Cómo continuar una sesión (instrucciones para el agente)

1. Lee este archivo + `supabase/migrations/001_init.sql` + `api/main.py`.
2. Ejecuta solo el PROMPT pedido. No mezcles módulos.
3. Verifica con: `python -m py_compile api/main.py`, `npx tsc --noEmit -p web` si existe, o `psql -f supabase/migrations/001_init.sql --dry-run` mental.
4. Al terminar, actualiza `docs/PROGRESS.md` con [x] y siguiente paso.

---

## PROMPT_01_CRUD (P1 — Inventario + fotos)

> Pégame esto cuando quieras que trabaje el CRUD:
> ```
> Lee 00_SYSTEM_PROMPT.md §0-§2. En rama minibase-web, implementa/verifica P1:
> web/app/(dashboard)/page.tsx grid oscuro + buscador + filtros tag/type/material,
> web/app/minis/[id]/page.tsx detalle + galería Cloudinary + lore + completeness bar,
> web/lib/supabase.ts + RLS, api/routers/minis.py CRUD + completeness_score,
> api/services/cloudinary_sign.py. Done = crear/editar/borrar/buscar mini con 3+ vistas funciona end-to-end.
> ```

## PROMPT_02_IMPORT (P2 — Excel/Drive + migración)

> ```
> Lee 00_SYSTEM_PROMPT.md §0-§2. En minibase-web implementa P2:
> api/routers/imports.py preview columnas (pandas) → mapping sugerido → upsert por slug,
> api/scripts/migrate_sqlite.py (lee src/miniatures.db + template.xlsx, corrige bug name[0]),
> web/app/imports/page.tsx upload + mapping UI + historial. Done = importar template.xlsx sin duplicados + ver historial.
> ```

## PROMPT_03_AGENT_API (P3 — API IA/CV-ready)

> ```
> Lee 00_SYSTEM_PROMPT.md §0-§2. En minibase-web implementa P3:
> supabase/migrations/002_vector.sql (pgvector + embeddings), api/routers/agent.py
> /agent/search semántico, /minis/{id}/dataset (multi-vista + phash + embedding),
> api/openapi_mcp.json. Done = GET /agent/search?query=dragon devuelve JSON + dataset con 13 vistas.
> ```

## PROMPT_04_CV_DATASET (futuro — reconocimiento webcam)

> ```
> Lee 00_SYSTEM_PROMPT.md. Implementa P4: api/services/vision.py calcula phash + CLIP embedding
> al subir imagen, supabase/migrations/003_vision.sql colas image_hash, endpoint
> POST /vision/match (imagen webcam → top-5 mini_ids). Done = foto frontal reconoce mini con >0.85.
> ```

## PROMPT_05_TABLE_STATE (futuro — proyector + máquina de estados)

> ```
> Lee 00_SYSTEM_PROMPT.md. Implementa P5: tabla table_state + api/routers/table.py
> GET/POST /table/state, web/app/table/page.tsx canvas proyector oscuro con grid solo si
> phase=movement + animaciones CSS. Done = cambiar fase desde DM enciende/apaga grid.
> ```

## Estado actual (actualizar cada sesión)

* [x] Rama `minibase-web` creada
* [x] Este pack + `supabase/001_init.sql` + scaffold `api/` + `web/`
* [ ] P1 end-to-end con credenciales reales
* [ ] P2 migración real `miniatures.db`
* [ ] P3 vector + MCP
