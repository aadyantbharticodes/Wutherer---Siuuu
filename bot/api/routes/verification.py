from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.verification import VerificationConfig

router = APIRouter(prefix="/guilds/{guild_id}/verification", tags=["Verification"], dependencies=[Depends(verify_api_key)])


class VerificationPatch(BaseModel):
    enabled: Optional[int] = None
    channel_id: Optional[int] = None
    role_id: Optional[int] = None
    difficulty: Optional[str] = None


@router.get("")
async def get_verification_config(guild_id: int, request: Request):
    bot = request.app.state.bot
    cfg = await VerificationConfig.get(bot.db, guild_id)
    return cfg


@router.patch("")
async def update_verification_config(guild_id: int, payload: VerificationPatch, request: Request):
    bot = request.app.state.bot
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if update_data:
        await VerificationConfig.update(bot.db, guild_id, **update_data)
    cfg = await VerificationConfig.get(bot.db, guild_id)
    return {"status": "success", "config": cfg}

