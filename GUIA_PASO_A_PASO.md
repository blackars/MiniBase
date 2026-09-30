# GUÍA PASO A PASO — las 3 cosas (tú las sacas, yo conecto)

Ya arreglé la demo: ahora + Nueva mini abre ficha completa (nombre, tipo mini|scenery|token|tile|prop,
cantidad, forma, bioforma, material, colores, alto/peso/base, escala, sistema RPG, facción, tags,
diseñador, pintor, año, ref, origen, historia, URL). Clic en tarjeta = ver detalle. Botones Editar/Borrar
funcionan. Todo se guarda en `api/demo_store.json` aunque reinicies la API demo.

Cuando quieras producción real (datos en nube + fotos Cloudinary + link https), haz esto:

## COSA 1 — Supabase (5 min, gratis)

1. Entra a https://supabase.com → Sign in con Google → New project.
   - Name: `minibase` — Password: inventa y guarda — Region: `South America (Sao Paulo)` — Free plan → Create.
   - Espera ~2 min a que diga Active.
2. Saca las claves NUEVAS (publishable + secret, anon/service_role es legacy):
   - Abajo izquierda engranaje `Project Settings` → pestaña `API` (o `Configuration > API`).
   - Arriba: `Project URL` (`https://xyz.supabase.co`) → DATO A.
   - En `API Keys`: `publishable` (empieza `sb_publishable_...`, dice Public) → DATO B. `Copy`.
   - En `API Keys`: `secret` (empieza `sb_secret_...`, dice Reveal primero) → DATO C. `Reveal` + `Copy`.
   - Si solo ves `anon / service_role`, es vista legacy: sirven igual (anon=publishable, service=secret), pero busca el toggle `New API keys`.
   - Pégamelos así: `URL=... / PUBLISHABLE=sb_publishable_... / SECRET=sb_secret_...`
3. Crea las tablas: a la izquierda SQL Editor → New query → abre en tu PC
   `supabase/migrations/001_init.sql` (rama minibase-web), copia TODO, pega, Run.
   Debe decir Success. Comprueba en Table Editor que ves `collections, miniatures, images…`
4. Activa login Google (para que cada base pida Auth):
   Authentication → Providers → Google → Enable. Te pedirá Client ID/Secret:
   - Ve a https://console.cloud.google.com → crea proyecto `minibase` → APIs → habilita Google+ API
     → Credentials → Create OAuth client → Web → añade en Authorized redirect:
     `https://xyz.supabase.co/auth/v1/callback` (xyz = tu URL) → copia ID y Secret a Supabase → Save.
   - Si esto te lía, sáltatelo hoy: la web funciona en modo demo sin login y lo activamos luego.

## COSA 2 — Cloudinary (3 min, ya lo manejas)

1. https://cloudinary.com/console → Settings → API Keys.
2. Copia `Cloud name` → DATO D, `API Key` → DATO E, `API Secret` (Reveal) → DATO F.
3. Settings → Upload → Upload presets → Add folder `minibase` (si no existe).
   No toques nada más: yo uso firma `signed` con path `minibase/{user}/{coleccion}/{slug}/{vista}`.
4. Pégame: `CLOUD_NAME=... / API_KEY=... / API_SECRET=...`

## COSA 3 — Despliegue Vercel por ti (10 min, gratis, te guío)

1. Sube la rama: en tu PC abre Git Bash en `MINIBASE/MiniBase` →
   `git add -A && git commit -m "minibase-web P1 demo" && git push -u origin minibase-web`
2. Entra a https://vercel.com → Sign in con GitHub → Add New Project → Import `blackars/MiniBase` →
   Branch: `minibase-web`, Root Directory: `MiniBase/web` (Edit) → Framework: Next.js → Deploy.
   Te dará `https://minibase-xxx.vercel.app` (provisional, sin API aún).
3. En ese proyecto Vercel → Settings → Environment Variables añade:
   `NEXT_PUBLIC_SUPABASE_URL` (=DATO A), `NEXT_PUBLIC_SUPABASE_ANON_KEY` (=DATO B),
   `NEXT_PUBLIC_API_URL` (= la URL de tu API, paso 4). Redeploy.
4. API en la nube (Render free): https://render.com → New Web Service → conecta tu repo →
   Root: `MiniBase/api`, Build: `pip install -r requirements.txt`, Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
   Añade envs: `SUPABASE_URL, SUPABASE_SERVICE_KEY, CLOUDINARY_*, CORS_ORIGINS=https://tu-vercel.app`.
   Te dará `https://minibase-api.onrender.com` → esa es la que pones en `NEXT_PUBLIC_API_URL`.
5. Vuelve a la web local `http://localhost:3000` con esas envs y verás “Supabase conectado” en vez de “modo demo”.

## Qué me pegas para que yo lo conecte

```
SUPABASE_URL=https://...
SUPABASE_ANON=...
SUPABASE_SERVICE=...
CLOUD_NAME=...
CLOUD_API_KEY=...
CLOUD_API_SECRET=...
```

Con eso yo cambio DEMO_STORE→Supabase, activo firma real Cloudinary + backup R2/Drive y te digo qué probar en el link.
