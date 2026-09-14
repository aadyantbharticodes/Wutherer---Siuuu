from __future__ import annotations
import json
from typing import Optional
from database.pool import DatabasePool


class LoggingConfigModel:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM logging_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute("INSERT OR IGNORE INTO logging_config (guild_id) VALUES (?)", guild_id)
            row = await db.fetchrow("SELECT * FROM logging_config WHERE guild_id = ?", guild_id)
        if not row:
            return {}
        d = dict(row)
        d["ignored_channels"] = json.loads(d.get("ignored_channels") or "[]")
        d["ignored_roles"] = json.loads(d.get("ignored_roles") or "[]")
        return d

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        if "ignored_channels" in kwargs and isinstance(kwargs["ignored_channels"], list):
            kwargs["ignored_channels"] = json.dumps(kwargs["ignored_channels"])
        if "ignored_roles" in kwargs and isinstance(kwargs["ignored_roles"], list):
            kwargs["ignored_roles"] = json.dumps(kwargs["ignored_roles"])
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE logging_config SET {sets} WHERE guild_id = ?", *vals)

