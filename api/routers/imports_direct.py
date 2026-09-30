"""Import directo: 1 upload -> bulk Postgres en segundos (sin chunks).

POST /api/imports/excel/direct {file, sheet?, dry_run?} con Bearer.
Hace diff server-side: idénticos se omiten con 0 writes.
"""
from fastapi import APIRouter, UploadFile, HTTPException, Request, Form
from fastapi.concurrency import run_in_threadpool
import json

router = APIRouter()


@router.post("/excel/direct")
async def direct(request: Request, file: UploadFile, sheet: str | None = Form(None),
                 dry_run: bool = Form(False), mapping: str | None = Form(None)):
    from services import db as _db
    from services import bulk_direct as _bulk
    if not (file.filename or "").lower().endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(400, "solo .xlsx / .xls / .csv")
    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(401, "login requerido")
    try:
        uid = _db.user_id_from_token(auth.split(" ", 1)[1].strip())
    except Exception:
        raise HTTPException(401, "token inválido")
    raw = await file.read()
    try:
        mmap = json.loads(mapping) if mapping else None
    except Exception:
        raise HTTPException(400, "mapping inválido (no es JSON)")
    try:
        return await run_in_threadpool(
            _bulk.bulk_upsert, raw, file.filename or "upload.xlsx",
            sheet, mmap, uid, bool(dry_run))
    except AssertionError as e:
        raise HTTPException(500, str(e))
    except Exception as e:
        raise HTTPException(500, f"bulk directo falló: {e}")
