from __future__ import annotations
from typing import Optional, Any
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Request

from api.auth import verify_api_key
from database.models.moderation import ModCases, Warnings, AutomodConfig, AntinukeConfig

router = APIRouter(prefix="/guilds/{guild_id}/moderation", tags=["Moderation"], dependencies=[Depends(verify_api_key)])


class AutomodPatch(BaseModel):
    antispam: Optional[int] = None
    anticaps: Optional[int] = None
    antilink: Optional[int] = None
    antiinvite: Optional[int] = None
    antimention: Optional[int] = None
    punishment: Optional[str] = None


class AntinukePatch(BaseModel):
    enabled: Optional[int] = None
    punishment: Optional[str] = None
    antibot: Optional[int] = None
    antiban: Optional[int] = None
    antikick: Optional[int] = None
    antichannel_create: Optional[int] = None
    antichannel_delete: Optional[int] = None


@router.get("/cases")
async def get_mod_cases(guild_id: int, request: Request, limit: int = 50):
    bot = request.app.state.bot
    cases = await ModCases.get_guild_cases(bot.db, guild_id, limit=limit)
    return cases


@router.get("/warnings/{user_id}")
async def get_user_warnings(guild_id: int, user_id: int, request: Request):
    bot = request.app.state.bot
    warns = await Warnings.get(bot.db, guild_id, user_id)
    return warns


@router.get("/automod")
async def get_automod_config(guild_id: int, request: Request):
    bot = request.app.state.bot
    cfg = await AutomodConfig.get(bot.db, guild_id)
    return cfg


@router.patch("/automod")
async def update_automod_config(guild_id: int, payload: AutomodPatch, request: Request):
    bot = request.app.state.bot
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if update_data:
        await AutomodConfig.update(bot.db, guild_id, **update_data)
    cfg = await AutomodConfig.get(bot.db, guild_id)
    return {"status": "success", "config": cfg}


@router.get("/antinuke")
async def get_antinuke_config(guild_id: int, request: Request):
    bot = request.app.state.bot
    cfg = await AntinukeConfig.get(bot.db, guild_id)
    whitelist = await AntinukeConfig.get_whitelist(bot.db, guild_id)
    return {"config": cfg, "whitelist": whitelist}


@router.patch("/antinuke")
async def update_antinuke_config(guild_id: int, payload: AntinukePatch, request: Request):
    bot = request.app.state.bot
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if update_data:
        await AntinukeConfig.update(bot.db, guild_id, **update_data)
    cfg = await AntinukeConfig.get(bot.db, guild_id)
    return {"status": "success", "config": cfg}

