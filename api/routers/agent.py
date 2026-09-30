"""P3: búsqueda semántica + dataset para DM + ④ inbox de completitud."""
from fastapi import APIRouter, HTTPException, Request
router = APIRouter()

def _uid(request: Request) -> str:
  from services import db as _db
  auth = request.headers.get("authorization", "")
  if not auth.lower().startswith("bearer "):
    raise HTTPException(401, "login requerido")
  try:
    return _db.user_id_from_token(auth.split(" ", 1)[1].strip())
  except Exception:
    raise HTTPException(401, "token inválido")

@router.get("/missing")
def missing_inbox(request: Request, field: str = "", limit: int = 50, offset: int = 0):
  """Cola de campos faltantes para completar poco a poco desde cualquier sitio."""
  from services import db as _db
  uid = _uid(request)
  sb = _db.client()
  col_id, _ = _db.get_user_collection(uid)
  # minis del usuario para mapear nombres (paginado liviano)
  names: dict[str, str] = {}
  off = 0
  while True:
    page = sb.table("miniatures").select("id,name").eq("collection_id", col_id) \
      .order("name").range(off, off + 999).execute().data or []
    if not page:
      break
    off += len(page)
    for r in page:
      names[r["id"]] = r["name"]
  ids = list(names.keys())
  total = 0
  items = []
  # missing_fields con join manual por mini (paginado por bloques de minis)
  for i in range(0, len(ids), 100):
    chunk = ids[i:i + 100]
    q = sb.table("missing_fields").select("*").in_("miniature_id", chunk).eq("status", "open")
    if field:
      q = q.eq("field_name", field)
    rows = q.order("miniature_id").execute().data or []
    total += len(rows)
    for r in rows:
      r["miniature_name"] = names.get(r["miniature_id"], "?")
      items.append(r)
  items.sort(key=lambda r: (r["miniature_name"], r["field_name"]))
  return {"total": total, "items": items[offset:offset + limit],
          "fields": sorted({r["field_name"] for r in items})}

@router.post("/missing/{mid}/resolve")
def resolve_missing(mid: str, payload: dict, request: Request):
  """Guarda el valor en la mini, cierra el faltante y recalcula completitud."""
  from services import db as _db
  from routers.minis import MiniIn, completeness
  from routers.imports import clean_tags, clean_num, clean_int, clean_bool, clean_str
  uid = _uid(request)
  sb = _db.client()
  rows = sb.table("missing_fields").select("*").eq("id", mid).eq("status", "open") \
    .limit(1).execute().data
  if not rows:
    raise HTTPException(404, "faltante no existe o ya resuelto")
  miss = rows[0]
  mini = _db.sb_get_mini(miss["miniature_id"], user_id=uid)
  fname = miss["field_name"]
  raw = payload.get("value", "")
  if fname == "tags":
    mini[fname] = clean_tags(raw)
  elif fname in ("weight_g", "height_mm", "radius_of_base_mm"):
    mini[fname] = clean_num(raw)
  elif fname == "quantity":
    mini[fname] = clean_int(raw) or 1
  elif fname == "lore_is_canon":
    mini[fname] = clean_bool(raw)
  else:
    mini[fname] = clean_str(raw)
  merged = dict(mini)
  merged.update({"collection_id": "default", "stats": {}})
  m = MiniIn(**{k: merged.get(k) for k in MiniIn.model_fields})
  merged["completeness_score"] = completeness(m)
  updated = _db.sb_update_mini(mini["id"], merged, user_id=uid)
  sb.table("missing_fields").update({"status": "done"}).eq("id", mid).execute()
  return {"mini": updated, "closed": mid}

def _norm(s: str) -> str:
  import unicodedata
  return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()

SEEDS = [
  {"id": "demo-1", "slug": "dragon-rojo", "name": "Dragón Rojo", "type": "mini",
   "tags": ["Fantasy", "D&D"], "material": "resina", "main_color": "rojo",
   "completeness_score": 82, "story": "Guardián del paso norte"},
  {"id": "demo-2", "slug": "bosque-elfico", "name": "Bosque Élfico", "type": "scenery",
   "tags": ["Fantasy"], "material": "PLA", "main_color": "verde",
   "completeness_score": 64, "story": "Escenografía modular 3 piezas"},
  {"id": "demo-3", "slug": "token-trampa", "name": "Token Trampa", "type": "token",
   "tags": ["D&D"], "material": "cartón", "main_color": "marrón",
   "completeness_score": 45, "story": "Token reversible"},
]

@router.get("/search")
def search(query: str = "", collection_id: str = "default", limit: int = 12):
  # Demo-local: busca en DEMO_STORE; con SUPABASE_URL usará pgvector (P3 completo)
  try:
    from .minis import DEMO_STORE
  except Exception:
    DEMO_STORE = {}
  items = list(DEMO_STORE.values()) or SEEDS
  if query:
    ql = _norm(query)
    items = [x for x in items if ql in _norm(x.get("name","")) or ql in _norm(x.get("tags",[])) or ql in _norm(x.get("story",""))]
  return {"query": query, "items": items[:limit], "mode": "demo-local"}

@router.post("/scenario")
def scenario(payload: dict):
  # DM futuro: solo usa inventario real -> consulta minis + lore
  ids = payload.get("mini_ids", [])
  return {"title": "Escenario con tu inventario",
    "cast": ids, "beats": [],
    "note": "P3+: LLM genera historia solo con dataset de esos ids."}
