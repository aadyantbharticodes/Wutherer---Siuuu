from __future__ import annotations
import json
from typing import Optional
from database.pool import DatabasePool


class PollModel:
    @staticmethod
    async def create(
        db: DatabasePool,
        guild_id: int,
        channel_id: int,
        message_id: int,
        creator_id: int,
        question: str,
        options: list[str],
        ends_at: Optional[str] = None
    ) -> int:
        return await db.execute(
            """INSERT INTO polls
               (guild_id, channel_id, message_id, creator_id, question, options, votes, ends_at)
               VALUES (?, ?, ?, ?, ?, ?, '{}', ?)""",
            guild_id, channel_id, message_id, creator_id, question, json.dumps(options), ends_at
        )

    @staticmethod
    async def get_by_message(db: DatabasePool, message_id: int) -> Optional[dict]:
        row = await db.fetchrow("SELECT * FROM polls WHERE message_id = ?", message_id)
        if not row:
            return None
        d = dict(row)
        d["options"] = json.loads(d.get("options") or "[]")
        d["votes"] = json.loads(d.get("votes") or "{}")
        return d

    @staticmethod
    async def vote(db: DatabasePool, message_id: int, user_id: int, option_idx: int) -> dict:
        poll = await PollModel.get_by_message(db, message_id)
        if not poll or poll["ended"]:
            return {}
        votes = poll["votes"]
        votes[str(user_id)] = option_idx
        await db.execute("UPDATE polls SET votes = ? WHERE message_id = ?", json.dumps(votes), message_id)
        return votes

    @staticmethod
    async def end_poll(db: DatabasePool, message_id: int) -> None:
        await db.execute("UPDATE polls SET ended = 1 WHERE message_id = ?", message_id)

