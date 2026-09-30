-- 004_bulk_keys.sql — Clave estable + hash para carga masiva semanal.
-- Idempotente. Correr en SQL Editor o vía conexión directa (pooler).
-- Resuelve: slug inestable por renombres + re-escritura de idénticos.

alter table public.miniatures add column if not exists external_key text;
alter table public.miniatures add column if not exists row_hash text;

do $$
begin
  if not exists (select 1 from pg_indexes where indexname = 'uq_minis_extkey') then
    create unique index uq_minis_extkey
      on public.miniatures(collection_id, external_key)
      where external_key is not null;
  end if;
  if not exists (select 1 from pg_indexes where indexname = 'idx_minis_exthash') then
    create index idx_minis_exthash
      on public.miniatures(collection_id, external_key, row_hash);
  end if;
  if not exists (select 1 from pg_indexes where indexname = 'idx_minis_slug') then
    create index idx_minis_slug on public.miniatures(collection_id, slug);
  end if;
end $$;

-- Backfill: external_key desde lore.code_or_reference normalizado (una vez).
-- Solo donde el código es ÚNICO dentro de la colección; duplicados reales
-- (ej. 'F', 'x2') quedan en NULL y usan slug como identidad (sin romper nada).
with uniq as (
  select m2.collection_id as cid, nullif(lower(trim(l.code_or_reference)), '') as code
  from public.miniatures m2
  join public.lore l on l.miniature_id = m2.id
  where nullif(lower(trim(l.code_or_reference)), '') is not null
  group by m2.collection_id, nullif(lower(trim(l.code_or_reference)), '')
  having count(*) = 1
)
update public.miniatures m
set external_key = nullif(lower(trim(l.code_or_reference)), '')
from public.lore l, uniq v
where l.miniature_id = m.id
  and m.collection_id = v.cid
  and nullif(lower(trim(l.code_or_reference)), '') = v.code
  and m.external_key is null;
