from __future__ import annotations
from typing import Optional
from database.pool import DatabasePool


class AIConfigModel:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM ai_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute("INSERT OR IGNORE INTO ai_config (guild_id) VALUES (?)", guild_id)
            row = await db.fetchrow("SELECT * FROM ai_config WHERE guild_id = ?", guild_id)
        return dict(row) if row else {}

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE ai_config SET {sets} WHERE guild_id = ?", *vals)

    @staticmethod
    async def add_history(db: DatabasePool, guild_id: int, user_id: int, role: str, content: str) -> None:
        await db.execute(
            "INSERT INTO ai_conversations (guild_id, user_id, role, content) VALUES (?, ?, ?, ?)",
            guild_id, user_id, role, content
        )

    @staticmethod
    async def get_history(db: DatabasePool, guild_id: int, user_id: int, limit: int = 10) -> list[dict]:
        rows = await db.fetch(
            """SELECT role, content FROM ai_conversations
               WHERE guild_id = ? AND user_id = ? 
               ORDER BY id DESC LIMIT ?""",
            guild_id, user_id, limit
        )
        return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

    @staticmethod
    async def clear_history(db: DatabasePool, guild_id: int, user_id: int) -> None:
        await db.execute(
            "DELETE FROM ai_conversations WHERE guild_id = ? AND user_id = ?",
            guild_id, user_id
        )

