"""Bootstrap Supabase: crea usuario auth (admin) + fila public.users + colección default.
Uso: python scripts/bootstrap_supabase.py [email]
Requiere api/.env con SUPABASE_URL + SUPABASE_SECRET_KEY.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from services import db


def main(email: str):
  sb = db.client()
  assert sb is not None, "sin cliente supabase: revisa api/.env"
  # 1. Usuario auth (si ya existe, lo reutiliza)
  try:
    res = sb.auth.admin.create_user({
      "email": email, "password": "MiniBase-Temporal-123",
      "email_confirm": True, "user_metadata": {"name": "MiniBase Owner"}})
    user = res.user
    print(f"auth user creado: {user.id} {user.email}")
  except Exception as e:
    print(f"create_user falló (quizá ya existe): {e}")
    lst = sb.auth.admin.list_users()
    cand = [u for u in (lst.users if hasattr(lst, "users") else lst) if getattr(u, "email", "") == email]
    assert cand, f"no existe {email} y no se pudo crear: {e}"
    user = cand[0]
    print(f"auth user reutilizado: {user.id} {user.email}")
  uid = user.id
  # 2. Fila public.users
  try:
    sb.table("users").upsert(
      {"id": uid, "email": email, "name": "MiniBase Owner"},
      on_conflict="id").execute()
    print("public.users ok")
  except Exception as e:
    print(f"public.users: {e}")
  # 3. Colección default
  ex = sb.table("collections").select("id").eq("user_id", uid).limit(1).execute()
  if ex.data:
    print(f"colección existente: {ex.data[0]['id']}")
  else:
    ins = sb.table("collections").insert({
      "user_id": uid, "name": "Mi colección",
      "description": "Colección principal MiniBase Web"}).execute()
    print(f"colección creada: {ins.data[0]['id']}")
  print("BOOTSTRAP OK — is_live:", db.is_live())


if __name__ == "__main__":
  main(sys.argv[1] if len(sys.argv) > 1 else "oscar.minibase@gmail.com")
