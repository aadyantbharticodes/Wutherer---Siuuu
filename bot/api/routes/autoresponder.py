from __future__ import annotations

from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Request

from api.auth import verify_api_key
from database.models.autoresponder import AutoResponderModel

router = APIRouter(prefix="/guilds/{guild_id}/autoresponder", tags=["AutoResponder"], dependencies=[Depends(verify_api_key)])


class TriggerCreate(BaseModel):
    trigger_text: str
    response_text: str
    match_mode: str = "exact"
    is_embed: bool = False
    cooldown_seconds: int = 5
    delete_trigger: bool = False


@router.get("/triggers")
async def list_triggers(guild_id: int, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = AutoResponderModel(db)
        triggers = await dao.list_triggers(guild_id)
        return [
            {
                "trigger_id": t.trigger_id,
                "trigger_text": t.trigger_text,
                "response_text": t.response_text,
                "match_mode": t.match_mode,
                "is_embed": t.is_embed,
                "cooldown_seconds": t.cooldown_seconds,
                "delete_trigger": t.delete_trigger,
                "enabled": t.enabled,
                "uses_count": t.uses_count,
            }
            for t in triggers
        ]


@router.post("/triggers")
async def create_trigger(guild_id: int, payload: TriggerCreate, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = AutoResponderModel(db)
        trigger_id = await dao.add_trigger(
            guild_id=guild_id,
            trigger_text=payload.trigger_text,
            response_text=payload.response_text,
            match_mode=payload.match_mode,
            is_embed=payload.is_embed,
            cooldown_seconds=payload.cooldown_seconds,
            delete_trigger=payload.delete_trigger,
        )
        return {"status": "success", "trigger_id": trigger_id}


@router.delete("/triggers/{trigger_id}")
async def delete_trigger(guild_id: int, trigger_id: int, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = AutoResponderModel(db)
        deleted = await dao.delete_trigger(trigger_id, guild_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Trigger not found")
        return {"status": "success", "deleted": True}

