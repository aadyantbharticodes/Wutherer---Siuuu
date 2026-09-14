from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Request

from api.auth import verify_api_key
from database.models.guild import GuildSettings, WelcomeConfig

router = APIRouter(prefix="/guilds", tags=["Guilds"], dependencies=[Depends(verify_api_key)])


class GuildSettingsPatch(BaseModel):
    prefix: Optional[str] = None
    language: Optional[str] = None
    log_channel_id: Optional[int] = None
    mod_log_channel_id: Optional[int] = None
    suggestion_channel_id: Optional[int] = None
    starboard_channel_id: Optional[int] = None
    starboard_threshold: Optional[int] = None


@router.get("")
async def list_guilds(request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        return []
    return [
        {
            "id": str(g.id),
            "name": g.name,
            "icon": g.icon.url if g.icon else None,
            "member_count": g.member_count,
            "owner_id": str(g.owner_id)
        }
        for g in bot.guilds
    ]


@router.get("/{guild_id}")
async def get_guild_details(guild_id: int, request: Request):
    bot = getattr(request.app.state, "bot", None)
    guild = bot.get_guild(guild_id) if bot else None
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    settings = await GuildSettings.get(bot.db, guild_id)
    welcome = await WelcomeConfig.get(bot.db, guild_id)

    channels = [
        {"id": str(c.id), "name": c.name, "type": str(c.type)}
        for c in guild.channels
    ]
    roles = [
        {"id": str(r.id), "name": r.name, "color": r.color.value}
        for r in guild.roles if not r.is_default()
    ]

    return {
        "id": str(guild.id),
        "name": guild.name,
        "icon": guild.icon.url if guild.icon else None,
        "member_count": guild.member_count,
        "settings": settings,
        "welcome": welcome,
        "channels": channels,
        "roles": roles
    }


@router.patch("/{guild_id}/settings")
async def update_guild_settings(guild_id: int, payload: GuildSettingsPatch, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot unavailable")

    update_dict = {k: v for k, v in payload.dict().items() if v is not None}
    if update_dict:
        await GuildSettings.update(bot.db, guild_id, **update_dict)
    updated = await GuildSettings.get(bot.db, guild_id)
    return {"status": "success", "settings": updated}

