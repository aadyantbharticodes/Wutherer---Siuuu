from __future__ import annotations
import json
from typing import Optional, Any
from database.pool import DatabasePool


class AntiAltModel:
    @staticmethod
    async def get_config(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM antialt_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute("INSERT OR IGNORE INTO antialt_config (guild_id) VALUES (?)", guild_id)
            await db.commit()
            row = await db.fetchrow("SELECT * FROM antialt_config WHERE guild_id = ?", guild_id)
        res = dict(row) if row else {
            "guild_id": guild_id,
            "enabled": 0,
            "min_age_days": 7,
            "require_avatar": 0,
            "action_type": "quarantine",
            "log_channel_id": None,
            "exempt_roles_json": "[]"
        }
        try:
            res["exempt_roles"] = json.loads(res["exempt_roles_json"]) if res.get("exempt_roles_json") else []
        except Exception:
            res["exempt_roles"] = []
        return res

    @staticmethod
    async def update_config(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        if "exempt_roles" in kwargs:
            kwargs["exempt_roles_json"] = json.dumps(kwargs.pop("exempt_roles"))
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE antialt_config SET {sets} WHERE guild_id = ?", *vals)
        await db.commit()

    @staticmethod
    async def add_log(
        db: DatabasePool,
        guild_id: int,
        user_id: int,
        account_age_days: int,
        action_taken: str,
        reason: str
    ) -> None:
        await db.execute(
            """INSERT INTO antialt_logs (guild_id, user_id, account_age_days, action_taken, reason)
               VALUES (?, ?, ?, ?, ?)""",
            guild_id,
            user_id,
            account_age_days,
            action_taken,
            reason
        )
        await db.commit()

    @staticmethod
    async def get_logs(db: DatabasePool, guild_id: int, limit: int = 50) -> list[dict]:
        rows = await db.fetch(
            "SELECT * FROM antialt_logs WHERE guild_id = ? ORDER BY id DESC LIMIT ?",
            guild_id,
            limit
        )
        return [dict(r) for r in rows]
