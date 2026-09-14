from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.youtube import YouTubeSubscription

router = APIRouter(prefix="/guilds/{guild_id}/youtube", tags=["YouTube"], dependencies=[Depends(verify_api_key)])


class YouTubeSubCreate(BaseModel):
    channel_id_yt: str
    channel_name: str
    notify_channel_id: int
    notify_role_id: Optional[int] = None
    custom_message: Optional[str] = None


@router.get("")
async def get_guild_youtube_subs(guild_id: int, request: Request):
    bot = request.app.state.bot
    subs = await YouTubeSubscription.get_by_guild(bot.db, guild_id)
    return subs


@router.post("")
async def add_youtube_subscription(guild_id: int, payload: YouTubeSubCreate, request: Request):
    bot = request.app.state.bot
    sub_id = await YouTubeSubscription.add(
        bot.db,
        guild_id,
        payload.channel_id_yt,
        payload.channel_name,
        payload.notify_channel_id,
        payload.notify_role_id,
        payload.custom_message
    )
    return {"status": "success", "id": sub_id}


@router.delete("/{channel_id_yt}")
async def remove_youtube_subscription(guild_id: int, channel_id_yt: str, request: Request):
    bot = request.app.state.bot
    await YouTubeSubscription.remove(bot.db, guild_id, channel_id_yt)
    return {"status": "success"}

