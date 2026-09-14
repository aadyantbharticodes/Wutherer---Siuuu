from __future__ import annotations
from typing import Optional
from database.pool import DatabasePool


class StarboardModel:
    @staticmethod
    async def get_entry(db: DatabasePool, original_message_id: int) -> Optional[dict]:
        row = await db.fetchrow(
            "SELECT * FROM starboard_entries WHERE original_message_id = ?",
            original_message_id
        )
        return dict(row) if row else None

    @staticmethod
    async def create_entry(
        db: DatabasePool,
        original_message_id: int,
        guild_id: int,
        channel_id: int,
        author_id: int,
        starboard_message_id: int,
        star_count: int = 1
    ) -> None:
        await db.execute(
            """INSERT INTO starboard_entries
               (original_message_id, guild_id, channel_id, starboard_message_id, star_count, author_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            original_message_id, guild_id, channel_id, starboard_message_id, star_count, author_id
        )

    @staticmethod
    async def update_stars(db: DatabasePool, original_message_id: int, star_count: int) -> None:
        await db.execute(
            "UPDATE starboard_entries SET star_count = ? WHERE original_message_id = ?",
            star_count, original_message_id
        )

    @staticmethod
    async def delete_entry(db: DatabasePool, original_message_id: int) -> None:
        await db.execute(
            "DELETE FROM starboard_entries WHERE original_message_id = ?",
            original_message_id
        )

