from __future__ import annotations
from typing import Optional
from database.pool import DatabasePool


class EconomyModel:
    @staticmethod
    async def get_account(db: DatabasePool, guild_id: int, user_id: int) -> dict:
        row = await db.fetchrow(
            "SELECT * FROM economy WHERE guild_id = ? AND user_id = ?",
            guild_id, user_id
        )
        if not row:
            await db.execute(
                "INSERT OR IGNORE INTO economy (guild_id, user_id, wallet, bank) VALUES (?, ?, 100, 0)",
                guild_id, user_id
            )
            row = await db.fetchrow("SELECT * FROM economy WHERE guild_id = ? AND user_id = ?", guild_id, user_id)
        return dict(row) if row else {"wallet": 0, "bank": 0, "last_daily": None, "last_work": None}

    @staticmethod
    async def modify_wallet(db: DatabasePool, guild_id: int, user_id: int, amount: int) -> int:
        await EconomyModel.get_account(db, guild_id, user_id)
        await db.execute(
            "UPDATE economy SET wallet = wallet + ? WHERE guild_id = ? AND user_id = ?",
            amount, guild_id, user_id
        )
        row = await db.fetchrow("SELECT wallet FROM economy WHERE guild_id = ? AND user_id = ?", guild_id, user_id)
        return row["wallet"] if row else 0

    @staticmethod
    async def modify_bank(db: DatabasePool, guild_id: int, user_id: int, amount: int) -> int:
        await EconomyModel.get_account(db, guild_id, user_id)
        await db.execute(
            "UPDATE economy SET bank = bank + ? WHERE guild_id = ? AND user_id = ?",
            amount, guild_id, user_id
        )
        row = await db.fetchrow("SELECT bank FROM economy WHERE guild_id = ? AND user_id = ?", guild_id, user_id)
        return row["bank"] if row else 0

    @staticmethod
    async def set_daily(db: DatabasePool, guild_id: int, user_id: int) -> None:
        await db.execute(
            "UPDATE economy SET last_daily = datetime('now') WHERE guild_id = ? AND user_id = ?",
            guild_id, user_id
        )

    @staticmethod
    async def set_work(db: DatabasePool, guild_id: int, user_id: int) -> None:
        await db.execute(
            "UPDATE economy SET last_work = datetime('now') WHERE guild_id = ? AND user_id = ?",
            guild_id, user_id
        )

    @staticmethod
    async def get_leaderboard(db: DatabasePool, guild_id: int, limit: int = 10) -> list[dict]:
        rows = await db.fetch(
            """SELECT user_id, wallet, bank, (wallet + bank) as total
               FROM economy WHERE guild_id = ? 
               ORDER BY total DESC LIMIT ?""",
            guild_id, limit
        )
        return [dict(r) for r in rows]

