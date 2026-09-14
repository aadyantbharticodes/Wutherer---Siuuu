from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from database.pool import DatabasePool


class GuildSettings:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchone(
            "SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,)
        )
        if row:
            return row
        await db.execute(
            "INSERT OR IGNORE INTO guild_settings (guild_id) VALUES (?)", (guild_id,)
        )
        await db.commit()
        return await db.fetchone(
            "SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,)
        ) or {"guild_id": guild_id, "prefix": "s!"}

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **fields) -> None:
        if not fields:
            return
        await GuildSettings.get(db, guild_id)
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [guild_id]
        await db.execute(
            f"UPDATE guild_settings SET {set_clause} WHERE guild_id = ?", tuple(values)
        )
        await db.commit()

    @staticmethod
    async def delete(db: DatabasePool, guild_id: int) -> None:
        await db.execute("DELETE FROM guild_settings WHERE guild_id = ?", (guild_id,))
        await db.commit()

