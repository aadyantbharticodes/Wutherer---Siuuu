from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.tickets import TicketConfig

router = APIRouter(prefix="/guilds/{guild_id}/tickets", tags=["Tickets"], dependencies=[Depends(verify_api_key)])


class TicketConfigPatch(BaseModel):
    enabled: Optional[int] = None
    category_id: Optional[int] = None
    log_channel_id: Optional[int] = None
    support_role_id: Optional[int] = None
    greeting: Optional[str] = None
    max_open: Optional[int] = None


@router.get("")
async def get_ticket_settings(guild_id: int, request: Request):
    bot = request.app.state.bot
    cfg = await TicketConfig.get(bot.db, guild_id)
    return cfg


@router.patch("")
async def update_ticket_settings(guild_id: int, payload: TicketConfigPatch, request: Request):
    bot = request.app.state.bot
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if update_data:
        await TicketConfig.update(bot.db, guild_id, **update_data)
    cfg = await TicketConfig.get(bot.db, guild_id)
    return {"status": "success", "config": cfg}

