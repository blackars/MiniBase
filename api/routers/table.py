"""P3/P5: máquina de estados simple para proyector. Grid solo en movement."""
from fastapi import APIRouter
router = APIRouter()
_STATE = {"phase": "story", "grid_visible": False, "tokens": []}

@router.get("/state")
def get_state(collection_id: str = ""):
  return {"collection_id": collection_id, **_STATE}

@router.post("/state")
def set_state(payload: dict):
  phase = payload.get("phase", "story")
  _STATE["phase"] = phase
  _STATE["grid_visible"] = (phase == "movement")
  if "tokens" in payload: _STATE["tokens"] = payload["tokens"]
  return _STATE
