"""Migra src/miniatures.db (SQLite) -> Supabase. Corrige bug (name[0])."""
import sqlite3, sys
from slugify import slugify
from pathlib import Path

def safe(v):
  if v is None: return None
  s = str(v).strip()
  return None if (not s or s.lower() in ("nan","none")) else s

def migrate(db_path: str):
  con = sqlite3.connect(db_path); con.row_factory = sqlite3.Row
  cur = con.cursor()
  rows = cur.execute("""
    SELECT m.id, m.name, v.*, l.* FROM miniature m
    LEFT JOIN visual_metadata v ON v.miniature_id=m.id
    LEFT JOIN lore l ON l.miniature_id=m.id""").fetchall()
  print(f"rows: {len(rows)}")
  for r in rows:
    name = safe(r["name"])  # FIX: antes creation_module hacía name[0]
    if not name: continue
    print(f"- {name} [{slugify(name)}] bioform={safe(r['bioform'])} shape={safe(r['shape'])}")
  print("TODO: upsert a Supabase via API /api/imports/excel/confirm")

if __name__ == "__main__":
  migrate(sys.argv[1] if len(sys.argv)>1 else "src/miniatures.db")
