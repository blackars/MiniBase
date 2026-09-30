"""Carga semanal directa: 1 transacción, segundos.
Uso:
  python scripts/bulk_upsert_excel.py <archivo.xlsx> [--sheet Hoja] [--dry-run]
Requiere api/.env con SUPABASE_URL + SUPABASE_DB_PASSWORD.
No usa chunks ni REST por fila: clasifica new/updated/identical y solo escribe cambios.
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    p = pathlib.Path(a.file)
    assert p.exists(), f"no existe {p}"
    from services import bulk_direct
    out = bulk_direct.bulk_upsert(
        p.read_bytes(), p.name, sheet=a.sheet, dry_run=a.dry_run)
    print(f"[{out['mode']}] hoja={out['sheet']} "
          f"nuevas={out['new']} actualizadas={out['updated']} "
          f"identicas_omitidas={out['skipped_identical']} omitidas={out['skipped']} "
          f"errores={out['n_errors']} tiempo={out['elapsed_s']}s")
    for e in out["errors"][:10]:
        print(" -", e)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
