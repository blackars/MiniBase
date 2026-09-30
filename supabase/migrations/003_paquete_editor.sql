-- 003_paquete_editor.sql — Paquete "editor central sin huecos" + base Plan 2.
-- Pegar en SQL Editor → Run. Idempotente (puede correrse 2 veces).

-- 1. Búsqueda rápida (Plan 2): trigramas + índices
create extension if not exists "pg_trgm";
create index if not exists idx_minis_name_trgm on public.miniatures using gin (name gin_trgm_ops);
create index if not exists idx_minis_collection_type on public.miniatures(collection_id, type);
create index if not exists idx_tags_name on public.tags(name);
create index if not exists idx_minitags_tag on public.miniature_tags(tag_id);
create index if not exists idx_missing_open on public.missing_fields(miniature_id, status);

-- 2. Faltantes sin duplicados futuros: 1 fila abierta por (mini, campo)
-- Deduplica primero (el camino REST viejo insertaba repetidos).
delete from public.missing_fields a using public.missing_fields b
where a.id > b.id
  and a.miniature_id = b.miniature_id
  and a.field_name = b.field_name
  and a.status = 'open' and b.status = 'open';
do $$
begin
  if not exists (select 1 from pg_indexes where indexname = 'uq_missing_open') then
    create unique index uq_missing_open on public.missing_fields(miniature_id, field_name)
    where status = 'open';
  end if;
end $$;

-- 3. Ledger de importaciones (anti re-subida + progreso reanudable)
alter table public.imports add column if not exists file_hash text;
alter table public.imports add column if not exists filename text;
alter table public.imports add column if not exists job_token text;
alter table public.imports add column if not exists total_rows int default 0;
alter table public.imports add column if not exists processed_rows int default 0;
do $$
begin
  if not exists (select 1 from pg_indexes where indexname = 'uq_imports_job') then
    create unique index uq_imports_job on public.imports(job_token) where job_token is not null;
  end if;
  if not exists (select 1 from pg_indexes where indexname = 'idx_imports_hash') then
    create index idx_imports_hash on public.imports(collection_id, file_hash);
  end if;
end $$;

-- 4. Imágenes por roles: fotos (entrenamiento) vs referencia (NO entrena).
--    Sintéticas etiquetadas NO se suben aquí: solo fotos, arte y 1 render de referencia.
alter table public.images add column if not exists role text not null default 'photo'
  check (role in ('photo', 'reference', 'video'));
alter table public.images alter column view_type drop not null;
do $$
begin
  begin
    alter table public.images drop constraint if exists images_view_type_check;
  exception when others then null;
  end;
  if not exists (select 1 from pg_constraint where conname = 'images_view_type_check2') then
    alter table public.images add constraint images_view_type_check2 check (
      view_type is null or view_type in (
        'frontal','black_background','white_background','lateral_1','lateral_2',
        'back_view','top_view','bottom_view','close_up','isometric','model_3d',
        'video_gif','other',
        -- referencia (no entran al set de entrenamiento):
        'render_3d','concept_art','paint_reference',
        -- contexto:
        'size_comparison','wip','packaging'));
  end if;
end $$;
create index if not exists idx_images_mini_role on public.images(miniature_id, role);

-- Verificación
select 'trgm' as ok where exists (select 1 from pg_extension where extname='pg_trgm');
select count(*) as minis from public.miniatures;
