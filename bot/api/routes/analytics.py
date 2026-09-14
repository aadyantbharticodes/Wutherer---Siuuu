from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.analytics import AnalyticsModel

router = APIRouter(prefix="/guilds/{guild_id}/analytics", tags=["Analytics"], dependencies=[Depends(verify_api_key)])


@router.get("/overview")
async def get_analytics_overview(guild_id: int, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = AnalyticsModel(db)
        totals = await dao.get_overview_totals(guild_id)
        recent_24h = await dao.get_recent_hourly(guild_id, hours=24)

    return {
        "guild_id": guild_id,
        "totals": totals,
        "hourly_24h": [
            {
                "timestamp": r.timestamp_hour,
                "messages": r.message_count,
                "voice_minutes": r.voice_minutes,
                "commands": r.commands_run,
            }
            for r in recent_24h
        ],
    }


@router.get("/channels")
async def get_top_channels(guild_id: int, request: Request, limit: int = 10):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = AnalyticsModel(db)
        top = await dao.get_top_channels(guild_id, limit=limit)
        return [
            {
                "channel_id": r.channel_id,
                "message_count": r.message_count,
                "last_active": r.last_active,
            }
            for r in top
        ]

