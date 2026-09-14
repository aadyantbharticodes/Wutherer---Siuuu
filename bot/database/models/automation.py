from __future__ import annotations
from typing import Optional
from database.pool import DatabasePool


class CustomCommands:
    @staticmethod
    async def add(
        db: DatabasePool,
        guild_id: int,
        name: str,
        response: str,
        created_by: int,
        embed_json: Optional[str] = None
    ) -> int:
        return await db.execute(
            """INSERT INTO custom_commands (guild_id, name, response, embed_json, created_by)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(guild_id, name) DO UPDATE SET
               response=excluded.response,
               embed_json=excluded.embed_json""",
            guild_id, name.lower(), response, embed_json, created_by
        )

    @staticmethod
    async def get(db: DatabasePool, guild_id: int, name: str) -> Optional[dict]:
        row = await db.fetchrow(
            "SELECT * FROM custom_commands WHERE guild_id = ? AND name = ?",
            guild_id, name.lower()
        )
        return dict(row) if row else None

    @staticmethod
    async def increment_uses(db: DatabasePool, cmd_id: int) -> None:
        await db.execute("UPDATE custom_commands SET uses = uses + 1 WHERE id = ?", cmd_id)

    @staticmethod
    async def delete(db: DatabasePool, guild_id: int, name: str) -> bool:
        res = await db.execute(
            "DELETE FROM custom_commands WHERE guild_id = ? AND name = ?",
            guild_id, name.lower()
        )
        return res > 0

    @staticmethod
    async def get_all(db: DatabasePool, guild_id: int) -> list[dict]:
        rows = await db.fetch("SELECT * FROM custom_commands WHERE guild_id = ? ORDER BY name ASC", guild_id)
        return [dict(r) for r in rows]


class StickyMessages:
    @staticmethod
    async def set(db: DatabasePool, guild_id: int, channel_id: int, content: str, embed_json: Optional[str] = None) -> None:
        await db.execute(
            """INSERT INTO sticky_messages (guild_id, channel_id, content, embed_json)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(channel_id) DO UPDATE SET
               content=excluded.content,
               embed_json=excluded.embed_json,
               counter=0""",
            guild_id, channel_id, content, embed_json
        )

    @staticmethod
    async def get(db: DatabasePool, channel_id: int) -> Optional[dict]:
        row = await db.fetchrow("SELECT * FROM sticky_messages WHERE channel_id = ?", channel_id)
        return dict(row) if row else None

    @staticmethod
    async def remove(db: DatabasePool, channel_id: int) -> None:
        await db.execute("DELETE FROM sticky_messages WHERE channel_id = ?", channel_id)

    @staticmethod
    async def update_message(db: DatabasePool, channel_id: int, message_id: int) -> None:
        await db.execute("UPDATE sticky_messages SET message_id = ?, counter = 0 WHERE channel_id = ?", message_id, channel_id)

