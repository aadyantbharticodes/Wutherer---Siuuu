from __future__ import annotations
from typing import Optional
from database.pool import DatabasePool


class YouTubeSubscription:
    @staticmethod
    async def add(
        db: DatabasePool,
        guild_id: int,
        channel_id_yt: str,
        channel_name: str,
        notify_channel_id: int,
        notify_role_id: Optional[int] = None,
        custom_message: Optional[str] = None,
    ) -> int:
        return await db.execute(
            """INSERT INTO youtube_subscriptions
               (guild_id, channel_id_yt, channel_name, notify_channel_id, notify_role_id, custom_message)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(guild_id, channel_id_yt) DO UPDATE SET
               notify_channel_id=excluded.notify_channel_id,
               notify_role_id=excluded.notify_role_id,
               custom_message=excluded.custom_message""",
            guild_id, channel_id_yt, channel_name, notify_channel_id, notify_role_id, custom_message
        )

    @staticmethod
    async def remove(db: DatabasePool, guild_id: int, channel_id_yt: str) -> None:
        await db.execute(
            "DELETE FROM youtube_subscriptions WHERE guild_id = ? AND channel_id_yt = ?",
            guild_id, channel_id_yt
        )

    @staticmethod
    async def get_by_guild(db: DatabasePool, guild_id: int) -> list[dict]:
        rows = await db.fetch(
            "SELECT * FROM youtube_subscriptions WHERE guild_id = ?",
            guild_id
        )
        return [dict(r) for r in rows]

    @staticmethod
    async def get_all_active(db: DatabasePool) -> list[dict]:
        rows = await db.fetch("SELECT * FROM youtube_subscriptions")
        return [dict(r) for r in rows]

    @staticmethod
    async def update_last_video(db: DatabasePool, sub_id: int, video_id: str) -> None:
        await db.execute(
            "UPDATE youtube_subscriptions SET last_video_id = ?, last_check = datetime('now') WHERE id = ?",
            video_id, sub_id
        )

