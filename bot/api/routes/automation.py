from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.automation import CustomCommands

router = APIRouter(prefix="/guilds/{guild_id}/automation", tags=["Automation"], dependencies=[Depends(verify_api_key)])


class CustomCommandCreate(BaseModel):
    name: str
    response: str


@router.get("/commands")
async def list_custom_commands(guild_id: int, request: Request):
    bot = request.app.state.bot
    cmds = await CustomCommands.get_all(bot.db, guild_id)
    return cmds


@router.post("/commands")
async def create_custom_command(guild_id: int, payload: CustomCommandCreate, request: Request):
    bot = request.app.state.bot
    cmd_id = await CustomCommands.add(bot.db, guild_id, payload.name, payload.response, created_by=0)
    return {"status": "success", "id": cmd_id}


@router.delete("/commands/{name}")
async def delete_custom_command(guild_id: int, name: str, request: Request):
    bot = request.app.state.bot
    deleted = await CustomCommands.delete(bot.db, guild_id, name)
    return {"status": "success", "deleted": deleted}

