from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.ai import AIConfigModel

router = APIRouter(prefix="/guilds/{guild_id}/ai", tags=["AI"], dependencies=[Depends(verify_api_key)])


class AIPatch(BaseModel):
    enabled: Optional[int] = None
    channel_id: Optional[int] = None
    persona: Optional[str] = None
    cooldown: Optional[int] = None


@router.get("")
async def get_ai_config(guild_id: int, request: Request):
    bot = request.app.state.bot
    cfg = await AIConfigModel.get(bot.db, guild_id)
    return cfg


@router.patch("")
async def update_ai_config(guild_id: int, payload: AIPatch, request: Request):
    bot = request.app.state.bot
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if update_data:
        await AIConfigModel.update(bot.db, guild_id, **update_data)
    cfg = await AIConfigModel.get(bot.db, guild_id)
    return {"status": "success", "config": cfg}

