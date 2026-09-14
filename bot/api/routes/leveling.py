from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.leveling import LevelingConfig, UserLevels

router = APIRouter(prefix="/guilds/{guild_id}/leveling", tags=["Leveling"], dependencies=[Depends(verify_api_key)])


class LevelingPatch(BaseModel):
    enabled: Optional[int] = None
    channel_id: Optional[int] = None
    announce_levelup: Optional[int] = None
    xp_rate: Optional[float] = None


@router.get("")
async def get_leveling_config(guild_id: int, request: Request):
    bot = request.app.state.bot
    cfg = await LevelingConfig.get(bot.db, guild_id)
    return cfg


@router.patch("")
async def update_leveling_config(guild_id: int, payload: LevelingPatch, request: Request):
    bot = request.app.state.bot
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if update_data:
        await LevelingConfig.update(bot.db, guild_id, **update_data)
    cfg = await LevelingConfig.get(bot.db, guild_id)
    return {"status": "success", "config": cfg}


@router.get("/leaderboard")
async def get_level_leaderboard(guild_id: int, request: Request, limit: int = 50):
    bot = request.app.state.bot
    lb = await UserLevels.get_leaderboard(bot.db, guild_id, limit=limit)
    return lb

