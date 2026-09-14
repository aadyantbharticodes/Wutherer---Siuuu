from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.antiphishing import AntiPhishingModel, AntiPhishingConfig

router = APIRouter(prefix="/guilds/{guild_id}/antiphishing", tags=["AntiPhishing"], dependencies=[Depends(verify_api_key)])


class AntiPhishingUpdate(BaseModel):
    enabled: bool
    action: str = "timeout"
    timeout_duration: int = 3600
    log_channel_id: Optional[int] = None
    whitelisted_domains: List[str] = []
    alert_staff: bool = True


@router.get("/config")
async def get_antiphishing_config(guild_id: int, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = AntiPhishingModel(db)
        cfg = await dao.get_config(guild_id)
        return {
            "guild_id": cfg.guild_id,
            "enabled": cfg.enabled,
            "action": cfg.action,
            "timeout_duration": cfg.timeout_duration,
            "log_channel_id": cfg.log_channel_id,
            "whitelisted_domains": cfg.whitelisted_domains,
            "custom_blacklisted_domains": cfg.custom_blacklisted_domains,
            "alert_staff": cfg.alert_staff,
        }


@router.put("/config")
async def update_antiphishing_config(guild_id: int, payload: AntiPhishingUpdate, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = AntiPhishingModel(db)
        config = AntiPhishingConfig(
            guild_id=guild_id,
            enabled=payload.enabled,
            action=payload.action,
            timeout_duration=payload.timeout_duration,
            log_channel_id=payload.log_channel_id,
            whitelisted_domains=payload.whitelisted_domains,
            alert_staff=payload.alert_staff,
        )
        await dao.save_config(config)
        return {"status": "success", "updated": True}

