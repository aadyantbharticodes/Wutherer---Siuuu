from __future__ import annotations

import uuid
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Request

from api.auth import verify_api_key
from database.models.backup import BackupModel, GuildBackupSnapshot

router = APIRouter(prefix="/guilds/{guild_id}/backups", tags=["Backups"], dependencies=[Depends(verify_api_key)])


class BackupCreate(BaseModel):
    notes: Optional[str] = None


@router.get("")
async def list_backups(guild_id: int, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = BackupModel(db)
        backups = await dao.list_guild_backups(guild_id)
        return [
            {
                "backup_id": b.backup_id,
                "guild_id": b.guild_id,
                "guild_name": b.guild_name,
                "created_by": b.created_by,
                "created_at": b.created_at,
                "roles_count": len(b.roles_data),
                "channels_count": len(b.channels_data),
                "categories_count": len(b.categories_data),
                "notes": b.notes,
            }
            for b in backups
        ]


@router.post("")
async def create_backup(guild_id: int, payload: BackupCreate, request: Request):
    """Capture the same guild structure exposed by the bot's backup command."""
    bot = request.app.state.bot
    guild = bot.get_guild(guild_id) if bot else None
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    roles = [
        {"id": role.id, "name": role.name, "color": role.color.value, "hoist": role.hoist,
         "mentionable": role.mentionable, "permissions": role.permissions.value, "position": role.position}
        for role in sorted(guild.roles, key=lambda item: item.position) if not role.is_default()
    ]
    categories = [{"id": category.id, "name": category.name, "position": category.position} for category in guild.categories]
    channels = [
        {"id": channel.id, "name": channel.name, "type": str(channel.type), "category_id": channel.category_id,
         "position": channel.position, "topic": getattr(channel, "topic", None), "nsfw": getattr(channel, "nsfw", False)}
        for channel in guild.channels if channel not in guild.categories
    ]
    snapshot = GuildBackupSnapshot(
        backup_id=f"snp_{uuid.uuid4().hex[:10]}", guild_id=guild.id, guild_name=guild.name,
        created_by=guild.owner_id or 0, roles_data=roles, categories_data=categories, channels_data=channels,
        emojis_data=[{"name": emoji.name, "url": str(emoji.url)} for emoji in guild.emojis[:50]], notes=payload.notes,
    )
    async with bot.db_pool.acquire() as db:
        await BackupModel(db).create_backup(snapshot)
    return {"status": "success", "backup_id": snapshot.backup_id}


@router.get("/{backup_id}")
async def get_backup_details(guild_id: int, backup_id: str, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = BackupModel(db)
        backup = await dao.get_backup(backup_id)
        if not backup or backup.guild_id != guild_id:
            raise HTTPException(status_code=404, detail="Backup not found")
        return {
            "backup_id": backup.backup_id,
            "guild_id": backup.guild_id,
            "guild_name": backup.guild_name,
            "created_by": backup.created_by,
            "created_at": backup.created_at,
            "roles": backup.roles_data,
            "categories": backup.categories_data,
            "channels": backup.channels_data,
            "emojis": backup.emojis_data,
            "notes": backup.notes,
        }


@router.delete("/{backup_id}")
async def delete_backup(guild_id: int, backup_id: str, request: Request):
    bot = request.app.state.bot
    async with bot.db_pool.acquire() as db:
        dao = BackupModel(db)
        deleted = await dao.delete_backup(backup_id, guild_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Backup not found or already deleted")
        return {"status": "success", "deleted": True}
