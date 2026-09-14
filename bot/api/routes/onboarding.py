from __future__ import annotations
from typing import Optional, Any
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from database.models.onboarding import AutoDMModel, AutoPingModel, AdvancedWelcomeModel

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


class UpdateAutoDMPayload(BaseModel):
    enabled: Optional[int] = None
    message: Optional[str] = None
    embed: Optional[dict] = None
    buttons: Optional[list[dict]] = None
    delay_seconds: Optional[int] = None


class UpdateAutoPingPayload(BaseModel):
    enabled: Optional[int] = None
    channels: Optional[list[int]] = None
    delete_after_seconds: Optional[int] = None
    ping_mode: Optional[str] = None
    message_template: Optional[str] = None


class UpdateWelcomePayload(BaseModel):
    farewell_enabled: Optional[int] = None
    farewell_channel_id: Optional[int] = None
    farewell_message: Optional[str] = None
    autorole_delay_minutes: Optional[int] = None
    autorole_delay_roles: Optional[list[int]] = None


@router.get("/{guild_id}")
async def get_onboarding_config(guild_id: int, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")

    autodm = await AutoDMModel.get(bot.db, guild_id)
    autoping = await AutoPingModel.get(bot.db, guild_id)
    welcome = await AdvancedWelcomeModel.get(bot.db, guild_id)

    return {
        "autodm": autodm,
        "autoping": autoping,
        "welcome": welcome
    }


@router.post("/{guild_id}/autodm")
async def update_autodm(guild_id: int, payload: UpdateAutoDMPayload, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if updates:
        await AutoDMModel.update(bot.db, guild_id, **updates)
    return {"success": True}


@router.post("/{guild_id}/autoping")
async def update_autoping(guild_id: int, payload: UpdateAutoPingPayload, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if updates:
        await AutoPingModel.update(bot.db, guild_id, **updates)
    return {"success": True}


@router.post("/{guild_id}/welcome")
async def update_welcome_advanced(guild_id: int, payload: UpdateWelcomePayload, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if updates:
        await AdvancedWelcomeModel.update(bot.db, guild_id, **updates)
    return {"success": True}
