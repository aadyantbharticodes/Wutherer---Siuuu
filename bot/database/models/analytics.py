from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import aiosqlite


@dataclass
class HourlyActivityRecord:
    guild_id: int
    timestamp_hour: int
    message_count: int = 0
    active_users: int = 0
    voice_minutes: int = 0
    commands_run: int = 0


@dataclass
class ChannelActivityRecord:
    guild_id: int
    channel_id: int
    message_count: int = 0
    last_active: int = 0


class AnalyticsModel:

    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def record_message_activity(self, guild_id: int, channel_id: int, user_id: int) -> None:
        now = int(time.time())
        hour_stamp = now - (now % 3600)


        query_hourly = """
            INSERT INTO analytics_hourly (guild_id, timestamp_hour, message_count, active_users, voice_minutes, commands_run)
            VALUES (?, ?, 1, 1, 0, 0)
            ON CONFLICT(guild_id, timestamp_hour) DO UPDATE SET
                message_count = message_count + 1
        """
        await self.db.execute(query_hourly, (guild_id, hour_stamp))


        query_channel = """
            INSERT INTO analytics_channels (guild_id, channel_id, message_count, last_active)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(guild_id, channel_id) DO UPDATE SET
                message_count = message_count + 1,
                last_active = ?
        """
        await self.db.execute(query_channel, (guild_id, channel_id, now, now))
        await self.db.commit()

    async def record_command_activity(self, guild_id: int) -> None:
        now = int(time.time())
        hour_stamp = now - (now % 3600)

        query = """
            INSERT INTO analytics_hourly (guild_id, timestamp_hour, message_count, active_users, voice_minutes, commands_run)
            VALUES (?, ?, 0, 0, 0, 1)
            ON CONFLICT(guild_id, timestamp_hour) DO UPDATE SET
                commands_run = commands_run + 1
        """
        await self.db.execute(query, (guild_id, hour_stamp))
        await self.db.commit()

    async def record_voice_minutes(self, guild_id: int, minutes: int) -> None:
        now = int(time.time())
        hour_stamp = now - (now % 3600)

        query = """
            INSERT INTO analytics_hourly (guild_id, timestamp_hour, message_count, active_users, voice_minutes, commands_run)
            VALUES (?, ?, 0, 0, ?, 0)
            ON CONFLICT(guild_id, timestamp_hour) DO UPDATE SET
                voice_minutes = voice_minutes + ?
        """
        await self.db.execute(query, (guild_id, hour_stamp, minutes, minutes))
        await self.db.commit()

    async def get_recent_hourly(self, guild_id: int, hours: int = 24) -> List[HourlyActivityRecord]:
        now = int(time.time())
        since_hour = (now - (now % 3600)) - (hours * 3600)

        query = """
            SELECT guild_id, timestamp_hour, message_count, active_users, voice_minutes, commands_run
            FROM analytics_hourly
            WHERE guild_id = ? AND timestamp_hour >= ?
            ORDER BY timestamp_hour ASC
        """
        async with self.db.execute(query, (guild_id, since_hour)) as cursor:
            rows = await cursor.fetchall()
            return [
                HourlyActivityRecord(
                    guild_id=r[0],
                    timestamp_hour=r[1],
                    message_count=r[2],
                    active_users=r[3],
                    voice_minutes=r[4],
                    commands_run=r[5],
                )
                for r in rows
            ]

    async def get_top_channels(self, guild_id: int, limit: int = 10) -> List[ChannelActivityRecord]:
        query = """
            SELECT guild_id, channel_id, message_count, last_active
            FROM analytics_channels
            WHERE guild_id = ?
            ORDER BY message_count DESC
            LIMIT ?
        """
        async with self.db.execute(query, (guild_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [
                ChannelActivityRecord(
                    guild_id=r[0],
                    channel_id=r[1],
                    message_count=r[2],
                    last_active=r[3],
                )
                for r in rows
            ]

    async def get_overview_totals(self, guild_id: int) -> Dict[str, int]:
        query = """
            SELECT 
                COALESCE(SUM(message_count), 0),
                COALESCE(SUM(voice_minutes), 0),
                COALESCE(SUM(commands_run), 0)
            FROM analytics_hourly
            WHERE guild_id = ?
        """
        async with self.db.execute(query, (guild_id,)) as cursor:
            row = await cursor.fetchone()
            return {
                "total_messages": row[0] if row else 0,
                "total_voice_minutes": row[1] if row else 0,
                "total_commands": row[2] if row else 0,
            }

