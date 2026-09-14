from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from api.auth import verify_api_key
from database.models.minecraft import MinecraftServerModel

router = APIRouter(prefix="/guilds/{guild_id}/minecraft", tags=["Minecraft"], dependencies=[Depends(verify_api_key)])


class MinecraftServerCreate(BaseModel):
    channel_id: int
    server_ip: str
    server_port: Optional[int] = None
    server_type: Optional[str] = "java"


@router.get("")
async def get_tracked_servers(guild_id: int, request: Request):
    bot = request.app.state.bot
    servers = await MinecraftServerModel.get_by_guild(bot.db, guild_id)
    return servers


@router.post("")
async def track_minecraft_server(guild_id: int, payload: MinecraftServerCreate, request: Request):
    bot = request.app.state.bot
    sid = await MinecraftServerModel.add(
        bot.db,
        guild_id,
        payload.channel_id,
        payload.server_ip,
        payload.server_port,
        payload.server_type or "java",
        setup_by=0
    )
    return {"status": "success", "id": sid}


@router.delete("/{server_ip}")
async def remove_minecraft_server(guild_id: int, server_ip: str, request: Request):
    bot = request.app.state.bot
    await MinecraftServerModel.remove(bot.db, guild_id, server_ip)
    return {"status": "success"}

