from __future__ import annotations
from typing import Optional
from database.pool import DatabasePool


class TicketConfig:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM ticket_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute(
                "INSERT OR IGNORE INTO ticket_config (guild_id) VALUES (?)",
                guild_id,
            )
            row = await db.fetchrow("SELECT * FROM ticket_config WHERE guild_id = ?", guild_id)
        return dict(row) if row else {}

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE ticket_config SET {sets} WHERE guild_id = ?", *vals)


class TicketManager:
    @staticmethod
    async def create(db: DatabasePool, guild_id: int, channel_id: int, user_id: int, subject: str = None) -> int:
        return await db.execute(
            "INSERT INTO tickets (guild_id, channel_id, user_id, subject) VALUES (?, ?, ?, ?)",
            guild_id, channel_id, user_id, subject or "Support"
        )

    @staticmethod
    async def get_by_channel(db: DatabasePool, channel_id: int) -> Optional[dict]:
        row = await db.fetchrow("SELECT * FROM tickets WHERE channel_id = ?", channel_id)
        return dict(row) if row else None

    @staticmethod
    async def get_open_tickets(db: DatabasePool, guild_id: int, user_id: int) -> list[dict]:
        rows = await db.fetch(
            "SELECT * FROM tickets WHERE guild_id = ? AND user_id = ? AND status = 'open'",
            guild_id, user_id
        )
        return [dict(r) for r in rows]

    @staticmethod
    async def claim(db: DatabasePool, channel_id: int, claimed_by: int) -> None:
        await db.execute("UPDATE tickets SET claimed_by = ? WHERE channel_id = ?", claimed_by, channel_id)

    @staticmethod
    async def close(db: DatabasePool, channel_id: int) -> None:
        await db.execute("UPDATE tickets SET status = 'closed', closed_at = datetime('now') WHERE channel_id = ?", channel_id)

