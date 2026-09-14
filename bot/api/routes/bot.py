from __future__ import annotations
import time
import discord
from fastapi import APIRouter, Depends, Request
from api.auth import verify_api_key

router = APIRouter(prefix="/bot", tags=["Bot"], dependencies=[Depends(verify_api_key)])


@router.get("/stats")
async def get_bot_stats(request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        return {"online": False}

    uptime_sec = int(time.time() - getattr(bot, "uptime_start", time.time()))
    return {
        "online": True,
        "username": str(bot.user),
        "id": bot.user.id if bot.user else None,
        "guilds": len(bot.guilds),
        "users": sum(g.member_count or 0 for g in bot.guilds),
        "uptime_seconds": uptime_sec,
        "latency_ms": round(bot.latency * 1000, 1),
    }

