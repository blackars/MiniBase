# EMPEZAR HOY — MiniBase Web (rama minibase-web)

Ya lo dejé corriendo en tu PC. No tienes que instalar nada más hoy.

## 1. Enlaces que ya funcionan (los encendí por ti)

* Web oscura demo: http://localhost:3000
* API: http://127.0.0.1:8000/health → `{"ok":true}`
* Swagger para probar P1-P3: http://127.0.0.1:8000/docs
  - `GET /api/agent/search?query=dragon` → trae Dragón Rojo demo
  - `POST /api/minis` → crear mini (botón + Crear en la web)
  - `GET /api/table/state` → `phase/story, grid_visible=false` (proyector futuro)
  - `GET /api/openapi_mcp.json` → tools para DM agéntico

Si cierras la PC se apagan. Para re-encender (2 doble-clics):
1. `api_INICIAR.bat` → enciende puerto 8000
2. `web_INICIAR.bat` → enciende puerto 3000

## 2. Probar hoy (5 min, sin claves)

1. Abre http://localhost:3000 → verás 3 demos: Dragón Rojo (mini), Bosque Élfico (scenery), Token Trampa (token).
2. Escribe `bosque` + Buscar → filtra por API real.
3. Escribe `Mi Orco` + botón + Crear → se guarda en memoria y aparece con barra de completitud.
4. Abre http://127.0.0.1:8000/docs → prueba `POST /api/imports/excel/preview` subiendo tu `template.xlsx`.

Todo es demo-local en memoria: al reiniciar API se borra. Es a propósito para que pruebes sin romper nada.

## 3. Para tener link de producción (lo hago yo, me faltan 3 datos)

No puedo crear un `https://...` público sin entrar a tus cuentas. En cuanto me pegues esto, lo despliego:

1. Supabase (ya lo has usado):
   - Crea proyecto free en https://supabase.com → Settings → API → cópiame `SUPABASE_URL`, `anon key`, `service_role key`
   - En SQL Editor pega `supabase/migrations/001_init.sql` → Run (crea tablas + RLS + pgvector)
   - Auth → Providers → Google → ON (para que cada colección pida login)
2. Cloudinary (ya lo manejas): `CLOUD_NAME`, `API_KEY`, `API_SECRET` (Settings → API Keys)
3. Vercel (para la web): dime si quieres que use tu cuenta o te guío a importar `web/` (1 clic, gratis).

Con eso yo: conecto `web/.env` + `api/.env`, cambio DEMO_STORE → Supabase, activo firma Cloudinary real + backup R2/Drive, y te devuelvo `https://minibase-web.vercel.app`.

## 4. Archivos clave en minibase-web

* `00_SYSTEM_PROMPT.md` → pégame `PROMPT_01/02/03` en futuras sesiones si pierdo contexto
* `supabase/migrations/001_init.sql` → schema futuro-proof (type mini|scenery|token, embedding, phash, rpg_profile JSONB, table_state)
* `api/main.py + routers/` → CRUD, imports Excel, agent search, table state
* `web/app/page.tsx` → dashboard oscuro que no exige login en demo, lo exigirá con Supabase real
* `docs/PROGRESS.md` → checklist P1-P3
