from __future__ import annotations
from typing import Optional
from database.pool import DatabasePool


class VerificationConfig:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM verification_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute("INSERT OR IGNORE INTO verification_config (guild_id) VALUES (?)", guild_id)
            row = await db.fetchrow("SELECT * FROM verification_config WHERE guild_id = ?", guild_id)
        return dict(row) if row else {}

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE verification_config SET {sets} WHERE guild_id = ?", *vals)

    @staticmethod
    async def record_attempt(db: DatabasePool, guild_id: int, user_id: int, success: bool, ip_hash: Optional[str] = None) -> None:
        await db.execute(
            "INSERT INTO verification_attempts (guild_id, user_id, success, ip_hash) VALUES (?, ?, ?, ?)",
            guild_id, user_id, 1 if success else 0, ip_hash
        )

    @staticmethod
    async def get_recent_failures(db: DatabasePool, guild_id: int, user_id: int, minutes: int = 15) -> int:
        row = await db.fetchrow(
            """SELECT COUNT(*) as count FROM verification_attempts
               WHERE guild_id = ? AND user_id = ? AND success = 0 
               AND created_at >= datetime('now', '-' || ? || ' minutes')""",
            guild_id, user_id, minutes
        )
        return row["count"] if row else 0

