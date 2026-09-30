-- MiniBase Web — 001_init.sql
-- Postgres 15 + pgvector. Compatible Supabase Free. RLS estricto por usuario.
-- Migra src/schema.sql (SQLite) a modelo futuro-proof para IA/CV/tablero.

create extension if not exists "pgcrypto";
create extension if not exists "vector";

-- Usuarios (espejo de auth.users)
create table public.users (
  id uuid primary key references auth.users(id) on delete cascade,
  email text not null,
  name text,
  avatar_url text,
  created_at timestamptz default now()
);

-- Colecciones: cada "base de datos de minis" exige Auth
create table public.collections (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  name text not null,
  description text,
  visibility text not null default 'private' check (visibility in ('private','shared')),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Miniatura principal. type permite scenery/tokens que pediste.
create table public.miniatures (
  id uuid primary key default gen_random_uuid(),
  collection_id uuid not null references public.collections(id) on delete cascade,
  name text not null,
  slug text not null,
  type text not null default 'mini' check (type in ('mini','scenery','token','tile','prop')),
  status text not null default 'active' check (status in ('active','wip','archived')),
  quantity int not null default 1,
  source text,
  external_id text,
  completeness_score int not null default 0,
  embedding vector(512),
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique(collection_id, slug)
);
create index idx_minis_collection on public.miniatures(collection_id);
create index idx_minis_type on public.miniatures(type);

-- Metadatos físicos/visuales (equivale a visual_metadata)
create table public.visual_metadata (
  id uuid primary key default gen_random_uuid(),
  miniature_id uuid not null unique references public.miniatures(id) on delete cascade,
  shape text, bioform text, material text,
  main_color text, secondary_color text,
  weight_g numeric, height_mm numeric, radius_of_base_mm numeric,
  base_shape text, scale text default '28mm',
  notes text
);

-- Imágenes multi-vista: Cloudinary primario + R2 backup + hash para CV
create table public.images (
  id uuid primary key default gen_random_uuid(),
  miniature_id uuid not null references public.miniatures(id) on delete cascade,
  view_type text not null check (view_type in
    ('frontal','black_background','white_background','lateral_1','lateral_2',
     'back_view','top_view','bottom_view','close_up','isometric','model_3d','video_gif','other')),
  cloudinary_public_id text not null,
  secure_url text not null,
  backup_url text,
  mime_type text, file_size int, width int, height int,
  phash text,
  created_at timestamptz default now(),
  unique(miniature_id, view_type, cloudinary_public_id)
);
create index idx_images_mini on public.images(miniature_id);

-- Lore enriquecido
create table public.lore (
  id uuid primary key default gen_random_uuid(),
  miniature_id uuid not null unique references public.miniatures(id) on delete cascade,
  designer text, painted_by text, label text,
  lore_is_canon boolean default false,
  character_origin text, story text, comment text,
  year text, code_or_reference text, url text, source_url text
);

-- Tags con categoría/color (evolución de tags plano)
create table public.tags (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  name text not null,
  category text, color text default '#888888', is_system boolean default false,
  created_at timestamptz default now(),
  unique(user_id, name)
);
create table public.miniature_tags (
  miniature_id uuid not null references public.miniatures(id) on delete cascade,
  tag_id uuid not null references public.tags(id) on delete cascade,
  primary key (miniature_id, tag_id)
);

-- Perfil RPG para DM agéntico + grid
create table public.rpg_profile (
  id uuid primary key default gen_random_uuid(),
  miniature_id uuid not null unique references public.miniatures(id) on delete cascade,
  system text, faction text, class text,
  stats jsonb default '{}'::jsonb,
  abilities jsonb default '[]'::jsonb,
  movement int, range_val int
);

-- Usos/preferencias (posibilidades de uso de cada mini)
create table public.gameplay_usage (
  id uuid primary key default gen_random_uuid(),
  miniature_id uuid not null unique references public.miniatures(id) on delete cascade,
  usable_as jsonb default '[]'::jsonb,
  preference int default 3,
  notes text
);

-- Trazabilidad importaciones Drive/Excel
create table public.data_sources (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  collection_id uuid references public.collections(id) on delete set null,
  drive_file_id text, drive_folder_id text, name text,
  mime_type text, last_synced_at timestamptz, mapping_config jsonb default '{}'::jsonb
);
create table public.imports (
  id uuid primary key default gen_random_uuid(),
  source_id uuid references public.data_sources(id) on delete set null,
  collection_id uuid references public.collections(id) on delete cascade,
  status text default 'done',
  rows_detected int default 0, rows_imported int default 0,
  rows_updated int default 0, rows_skipped int default 0,
  errors jsonb default '[]'::jsonb, warnings jsonb default '[]'::jsonb,
  started_at timestamptz default now(), finished_at timestamptz
);

-- Agente: faltantes + encuestas + tareas
create table public.missing_fields (
  id uuid primary key default gen_random_uuid(),
  miniature_id uuid not null references public.miniatures(id) on delete cascade,
  field_name text not null, severity text default 'medium',
  suggested_question text, status text default 'open'
);
create table public.surveys (
  id uuid primary key default gen_random_uuid(),
  collection_id uuid not null references public.collections(id) on delete cascade,
  title text not null, status text default 'open',
  created_at timestamptz default now(), completed_at timestamptz
);
create table public.survey_questions (
  id uuid primary key default gen_random_uuid(),
  survey_id uuid not null references public.surveys(id) on delete cascade,
  miniature_id uuid references public.miniatures(id) on delete cascade,
  field_name text, question text, answer_type text default 'text',
  options jsonb, answer text, status text default 'pending'
);
create table public.agent_tasks (
  id uuid primary key default gen_random_uuid(),
  collection_id uuid references public.collections(id) on delete cascade,
  task_type text, status text default 'pending',
  input jsonb, output jsonb,
  created_at timestamptz default now(), finished_at timestamptz
);

-- Estado del tablero proyectado (máquina de estados simple)
create table public.table_state (
  collection_id uuid primary key references public.collections(id) on delete cascade,
  phase text not null default 'story' check (phase in ('story','movement','combat','ended')),
  grid_visible boolean not null default false,
  tokens jsonb not null default '[]'::jsonb,
  updated_at timestamptz default now()
);

-- Seeds: NO insertar aquí (no hay users aún y tags.user_id es NOT NULL).
-- Los tags sistema se crean por usuario desde la app al crear su primera colección.
-- Ver api/routers/minis.py + web/app/page.tsx (tags por defecto: Sci-Fi, Fantasy, D&D...).

-- RLS
alter table public.users enable row level security;
alter table public.collections enable row level security;
alter table public.miniatures enable row level security;
alter table public.visual_metadata enable row level security;
alter table public.images enable row level security;
alter table public.lore enable row level security;
alter table public.tags enable row level security;
alter table public.miniature_tags enable row level security;
alter table public.rpg_profile enable row level security;
alter table public.gameplay_usage enable row level security;
alter table public.data_sources enable row level security;
alter table public.imports enable row level security;
alter table public.missing_fields enable row level security;
alter table public.surveys enable row level security;
alter table public.survey_questions enable row level security;
alter table public.agent_tasks enable row level security;
alter table public.table_state enable row level security;

-- Políticas: dueño ve/edita lo suyo. Colecciones shared legibles por link (token aparte en app).
create policy "own users" on public.users for all using (auth.uid() = id);
create policy "own collections" on public.collections for all using (auth.uid() = user_id);
create policy "own minis" on public.miniatures for all using (
  exists (select 1 from public.collections c where c.id = collection_id and c.user_id = auth.uid()));
create policy "own images" on public.images for all using (
  exists (select 1 from public.miniatures m join public.collections c on c.id = m.collection_id
          where m.id = miniature_id and c.user_id = auth.uid()));
create policy "own visual" on public.visual_metadata for all using (
  exists (select 1 from public.miniatures m join public.collections c on c.id = m.collection_id
          where m.id = miniature_id and c.user_id = auth.uid()));
create policy "own lore" on public.lore for all using (
  exists (select 1 from public.miniatures m join public.collections c on c.id = m.collection_id
          where m.id = miniature_id and c.user_id = auth.uid()));
create policy "own tags" on public.tags for all using (auth.uid() = user_id);
create policy "own minitags" on public.miniature_tags for all using (
  exists (select 1 from public.miniatures m join public.collections c on c.id = m.collection_id
          where m.id = miniature_id and c.user_id = auth.uid()));
create policy "own rpg" on public.rpg_profile for all using (
  exists (select 1 from public.miniatures m join public.collections c on c.id = m.collection_id
          where m.id = miniature_id and c.user_id = auth.uid()));
create policy "own usage" on public.gameplay_usage for all using (
  exists (select 1 from public.miniatures m join public.collections c on c.id = m.collection_id
          where m.id = miniature_id and c.user_id = auth.uid()));
create policy "own sources" on public.data_sources for all using (auth.uid() = user_id);
create policy "own imports" on public.imports for all using (
  exists (select 1 from public.collections c where c.id = collection_id and c.user_id = auth.uid()));
create policy "own missing" on public.missing_fields for all using (
  exists (select 1 from public.miniatures m join public.collections c on c.id = m.collection_id
          where m.id = miniature_id and c.user_id = auth.uid()));
create policy "own surveys" on public.surveys for all using (
  exists (select 1 from public.collections c where c.id = collection_id and c.user_id = auth.uid()));
create policy "own questions" on public.survey_questions for all using (
  exists (select 1 from public.surveys s join public.collections c on c.id = s.collection_id
          where s.id = survey_id and c.user_id = auth.uid()));
create policy "own tasks" on public.agent_tasks for all using (
  collection_id is null or exists (select 1 from public.collections c where c.id = collection_id and c.user_id = auth.uid()));
create policy "own tablestate" on public.table_state for all using (
  exists (select 1 from public.collections c where c.id = collection_id and c.user_id = auth.uid()));
