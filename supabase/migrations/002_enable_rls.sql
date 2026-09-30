-- 002_enable_rls.sql — PARCHE para quienes corrieron 001_init.sql con el seed roto.
-- Las tablas ya existen; solo falta activar RLS + políticas (el script original se detuvo en el INSERT).
-- Pégalo en SQL Editor → Run. Es idempotente: puedes correrlo 2 veces sin error.

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

drop policy if exists "own users" on public.users;
drop policy if exists "own collections" on public.collections;
drop policy if exists "own minis" on public.miniatures;
drop policy if exists "own images" on public.images;
drop policy if exists "own visual" on public.visual_metadata;
drop policy if exists "own lore" on public.lore;
drop policy if exists "own tags" on public.tags;
drop policy if exists "own minitags" on public.miniature_tags;
drop policy if exists "own rpg" on public.rpg_profile;
drop policy if exists "own usage" on public.gameplay_usage;
drop policy if exists "own sources" on public.data_sources;
drop policy if exists "own imports" on public.imports;
drop policy if exists "own missing" on public.missing_fields;
drop policy if exists "own surveys" on public.surveys;
drop policy if exists "own questions" on public.survey_questions;
drop policy if exists "own tasks" on public.agent_tasks;
drop policy if exists "own tablestate" on public.table_state;

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

-- Verificación: debe devolver 17 filas (una por tabla con RLS activo)
select tablename from pg_tables where schemaname='public' and rowsecurity order by tablename;
