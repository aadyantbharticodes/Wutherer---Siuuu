from __future__ import annotations
import json
from typing import Optional
from database.pool import DatabasePool


class GiveawayModel:
    @staticmethod
    async def create(
        db: DatabasePool,
        guild_id: int,
        channel_id: int,
        message_id: int,
        host_id: int,
        prize: str,
        winners: int,
        ends_at: str,
        required_role_id: Optional[int] = None
    ) -> int:
        return await db.execute(
            """INSERT INTO giveaways
               (guild_id, channel_id, message_id, host_id, prize, winners, ends_at, required_role_id, entries)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, '[]')""",
            guild_id, channel_id, message_id, host_id, prize, winners, ends_at, required_role_id
        )

    @staticmethod
    async def get_by_message(db: DatabasePool, message_id: int) -> Optional[dict]:
        row = await db.fetchrow("SELECT * FROM giveaways WHERE message_id = ?", message_id)
        if not row:
            return None
        data = dict(row)
        data["entries"] = json.loads(data.get("entries") or "[]")
        return data

    @staticmethod
    async def add_entry(db: DatabasePool, message_id: int, user_id: int) -> tuple[bool, int]:
        data = await GiveawayModel.get_by_message(db, message_id)
        if not data or data["ended"]:
            return False, 0
        entries = data["entries"]
        if user_id in entries:
            entries.remove(user_id)
            added = False
        else:
            entries.append(user_id)
            added = True
        await db.execute(
            "UPDATE giveaways SET entries = ? WHERE message_id = ?",
            json.dumps(entries), message_id
        )
        return added, len(entries)

    @staticmethod
    async def get_active(db: DatabasePool) -> list[dict]:
        rows = await db.fetch("SELECT * FROM giveaways WHERE ended = 0")
        results = []
        for r in rows:
            d = dict(r)
            d["entries"] = json.loads(d.get("entries") or "[]")
            results.append(d)
        return results

    @staticmethod
    async def end_giveaway(db: DatabasePool, message_id: int) -> None:
        await db.execute("UPDATE giveaways SET ended = 1 WHERE message_id = ?", message_id)

