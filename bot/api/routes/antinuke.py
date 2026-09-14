from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from database.models.antinuke import AntiNukeModel
from services.antinuke import AntiNukeService

router = APIRouter(prefix="/antinuke", tags=["AntiNuke"])


class UpdateAntiNukePayload(BaseModel):
    enabled: Optional[int] = None
    log_channel_id: Optional[int] = None
    quarantine_role_id: Optional[int] = None
    max_channel_deletes: Optional[int] = None
    max_role_deletes: Optional[int] = None
    max_bans: Optional[int] = None
    max_kicks: Optional[int] = None
    max_webhook_creates: Optional[int] = None
    rate_window_seconds: Optional[int] = None
    action_type: Optional[str] = None


class WhitelistPayload(BaseModel):
    entity_id: int
    entity_type: Optional[str] = "user"


class LockdownPayload(BaseModel):
    action: str = "lock"


@router.get("/{guild_id}")
async def get_antinuke_status(guild_id: int, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    cfg = await AntiNukeModel.get_config(bot.db, guild_id)
    whitelist = await AntiNukeModel.get_whitelist(bot.db, guild_id)
    return {"config": cfg, "whitelist": whitelist}


@router.post("/{guild_id}")
async def update_antinuke_config(guild_id: int, payload: UpdateAntiNukePayload, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if updates:
        await AntiNukeModel.update_config(bot.db, guild_id, **updates)
    return {"success": True}


@router.post("/{guild_id}/whitelist")
async def add_whitelist(guild_id: int, payload: WhitelistPayload, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    await AntiNukeModel.add_whitelist(bot.db, guild_id, payload.entity_id, payload.entity_type or "user")
    return {"success": True}


@router.delete("/{guild_id}/whitelist/{entity_id}")
async def remove_whitelist(guild_id: int, entity_id: int, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    await AntiNukeModel.remove_whitelist(bot.db, guild_id, entity_id)
    return {"success": True}


@router.get("/{guild_id}/logs")
async def get_security_logs(guild_id: int, request: Request, limit: int = 50):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    logs = await AntiNukeModel.get_logs(bot.db, guild_id, limit=limit)
    return {"logs": logs}


@router.post("/{guild_id}/lockdown")
async def toggle_panic_lockdown(guild_id: int, payload: LockdownPayload, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    guild = bot.get_guild(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    service = AntiNukeService(bot, bot.db)
    if payload.action.lower() == "unlock":
        res = await service.lift_lockdown(guild)
    else:
        res = await service.panic_lockdown(guild)

    return {"success": True, "results": res}
