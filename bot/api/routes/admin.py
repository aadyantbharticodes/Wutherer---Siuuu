from __future__ import annotations
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(verify_api_key)])


class ReloadModulePayload(BaseModel):
    module: str


@router.post("/reload")
async def reload_module(payload: ReloadModulePayload, request: Request):
    bot = request.app.state.bot
    mod = payload.module
    if not mod.startswith("extensions."):
        mod = f"extensions.{mod}"
    try:
        await bot.reload_extension(mod)
        return {"status": "success", "module": mod}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}

