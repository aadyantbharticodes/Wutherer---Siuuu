from __future__ import annotations
from typing import Optional
from database.pool import DatabasePool


class MinecraftServerModel:
    @staticmethod
    async def add(
        db: DatabasePool,
        guild_id: int,
        channel_id: int,
        server_ip: str,
        server_port: Optional[int] = None,
        server_type: str = "java",
        setup_by: int = 0,
        message_id: Optional[int] = None
    ) -> int:
        return await db.execute(
            """INSERT INTO minecraft_servers
               (guild_id, channel_id, server_ip, server_port, server_type, setup_by, message_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(guild_id, server_ip) DO UPDATE SET
               channel_id=excluded.channel_id,
               server_port=excluded.server_port,
               server_type=excluded.server_type,
               message_id=excluded.message_id""",
            guild_id, channel_id, server_ip, server_port, server_type, setup_by, message_id
        )

    @staticmethod
    async def get_by_guild(db: DatabasePool, guild_id: int) -> list[dict]:
        rows = await db.fetch("SELECT * FROM minecraft_servers WHERE guild_id = ?", guild_id)
        return [dict(r) for r in rows]

    @staticmethod
    async def get_all(db: DatabasePool) -> list[dict]:
        rows = await db.fetch("SELECT * FROM minecraft_servers WHERE auto_refresh = 1")
        return [dict(r) for r in rows]

    @staticmethod
    async def remove(db: DatabasePool, guild_id: int, server_ip: str) -> None:
        await db.execute(
            "DELETE FROM minecraft_servers WHERE guild_id = ? AND server_ip = ?",
            guild_id, server_ip
        )

    @staticmethod
    async def update_message_id(db: DatabasePool, server_id: int, message_id: int) -> None:
        await db.execute(
            "UPDATE minecraft_servers SET message_id = ? WHERE id = ?",
            message_id, server_id
        )

