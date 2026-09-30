"""Conexión directa Postgres (pooler Supabase) para carga masiva.

Solo servidor. Lee api/.env (SUPABASE_URL + SUPABASE_DB_PASSWORD).
Una conexión por job bulk (1 transacción), NO una por fila.
Nunca loguea el password.
"""
import os
import pathlib

POOLER_HOST = os.getenv("SUPABASE_POOLER_HOST", "aws-0-sa-east-1.pooler.supabase.com")
POOLER_PORT = int(os.getenv("SUPABASE_POOLER_PORT", "6543"))

_cache: dict = {}


def _load_env() -> dict:
    if _cache:
        return _cache
    p = pathlib.Path(__file__).parent.parent / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            _cache[k.strip()] = v.strip()
    for k in ("SUPABASE_URL", "SUPABASE_DB_PASSWORD",
              "SUPABASE_POOLER_HOST", "SUPABASE_POOLER_PORT"):
        if os.getenv(k):
            _cache[k] = os.getenv(k).strip()
    return _cache


def ref_from_url(url: str) -> str:
    return url.split("//")[-1].split(".")[0]


def get_conn():
    """Una conexión psycopg2 al pooler (transaction mode). Lanza si falta password."""
    import psycopg2
    env = _load_env()
    url = env.get("SUPABASE_URL", "")
    pwd = env.get("SUPABASE_DB_PASSWORD", "")
    assert url, "falta SUPABASE_URL en api/.env"
    assert pwd, "falta SUPABASE_DB_PASSWORD en api/.env (reset en Supabase → Settings → Database)"
    ref = ref_from_url(url)
    host = env.get("SUPABASE_POOLER_HOST", POOLER_HOST)
    port = int(env.get("SUPABASE_POOLER_PORT", POOLER_PORT))
    return psycopg2.connect(
        host=host, port=port, dbname="postgres",
        user=f"postgres.{ref}", password=pwd,
        connect_timeout=15, sslmode="require",
        options="-c statement_timeout=120000",
    )


def run_sql_file(path: str) -> None:
    """Ejecuta una migración .sql en una transacción (para 004)."""
    import pathlib as _pl
    sql = _pl.Path(path).read_text(encoding="utf-8")
    conn = get_conn()
    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(sql)
    finally:
        conn.close()
