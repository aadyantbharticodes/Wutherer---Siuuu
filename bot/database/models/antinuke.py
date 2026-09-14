from __future__ import annotations
import json
from typing import Optional, Any
from database.pool import DatabasePool


class AntiNukeModel:
    @staticmethod
    async def get_config(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM antinuke_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute(
                """INSERT OR IGNORE INTO antinuke_config (guild_id) VALUES (?)""",
                guild_id
            )
            await db.commit()
            row = await db.fetchrow("SELECT * FROM antinuke_config WHERE guild_id = ?", guild_id)
        return dict(row) if row else {
            "guild_id": guild_id,
            "enabled": 0,
            "log_channel_id": None,
            "quarantine_role_id": None,
            "max_channel_deletes": 3,
            "max_role_deletes": 3,
            "max_bans": 5,
            "max_kicks": 5,
            "max_webhook_creates": 2,
            "rate_window_seconds": 15,
            "action_type": "ban",
            "panic_lockdown_enabled": 0,
        }

    @staticmethod
    async def update_config(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE antinuke_config SET {sets} WHERE guild_id = ?", *vals)
        await db.commit()

    @staticmethod
    async def is_whitelisted(db: DatabasePool, guild_id: int, entity_id: int) -> bool:
        row = await db.fetchrow(
            "SELECT id FROM antinuke_whitelist WHERE guild_id = ? AND entity_id = ?",
            guild_id,
            entity_id
        )
        return row is not None

    @staticmethod
    async def add_whitelist(db: DatabasePool, guild_id: int, entity_id: int, entity_type: str = "user") -> bool:
        await db.execute(
            """INSERT OR IGNORE INTO antinuke_whitelist (guild_id, entity_id, entity_type)
               VALUES (?, ?, ?)""",
            guild_id,
            entity_id,
            entity_type
        )
        await db.commit()
        return True

    @staticmethod
    async def remove_whitelist(db: DatabasePool, guild_id: int, entity_id: int) -> bool:
        await db.execute(
            "DELETE FROM antinuke_whitelist WHERE guild_id = ? AND entity_id = ?",
            guild_id,
            entity_id
        )
        await db.commit()
        return True

    @staticmethod
    async def get_whitelist(db: DatabasePool, guild_id: int) -> list[dict]:
        rows = await db.fetch(
            "SELECT * FROM antinuke_whitelist WHERE guild_id = ? ORDER BY created_at DESC",
            guild_id
        )
        return [dict(r) for r in rows]

    @staticmethod
    async def add_log(
        db: DatabasePool,
        guild_id: int,
        culprit_id: int,
        event_type: str,
        details: str,
        action_taken: str
    ) -> None:
        await db.execute(
            """INSERT INTO antinuke_logs (guild_id, culprit_id, event_type, details, action_taken)
               VALUES (?, ?, ?, ?, ?)""",
            guild_id,
            culprit_id,
            event_type,
            details,
            action_taken
        )
        await db.commit()

    @staticmethod
    async def get_logs(db: DatabasePool, guild_id: int, limit: int = 50) -> list[dict]:
        rows = await db.fetch(
            "SELECT * FROM antinuke_logs WHERE guild_id = ? ORDER BY id DESC LIMIT ?",
            guild_id,
            limit
        )
        return [dict(r) for r in rows]

    @staticmethod
    async def save_lockdown_state(db: DatabasePool, guild_id: int, channel_id: int, overwrites: dict) -> None:
        await db.execute(
            """INSERT OR REPLACE INTO lockdown_state (guild_id, channel_id, overwrites_json)
               VALUES (?, ?, ?)""",
            guild_id,
            channel_id,
            json.dumps(overwrites)
        )
        await db.commit()

    @staticmethod
    async def get_lockdown_states(db: DatabasePool, guild_id: int) -> list[dict]:
        rows = await db.fetch(
            "SELECT * FROM lockdown_state WHERE guild_id = ?",
            guild_id
        )
        result = []
        for r in rows:
            item = dict(r)
            try:
                item["overwrites"] = json.loads(item["overwrites_json"])
            except Exception:
                item["overwrites"] = {}
            result.append(item)
        return result

    @staticmethod
    async def clear_lockdown_states(db: DatabasePool, guild_id: int) -> None:
        await db.execute("DELETE FROM lockdown_state WHERE guild_id = ?", guild_id)
        await db.commit()
