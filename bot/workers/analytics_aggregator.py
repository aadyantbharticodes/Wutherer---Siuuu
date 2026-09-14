from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from bot.database.models.analytics import AnalyticsModel

if TYPE_CHECKING:
    from bot.core.bot import WuthererBot

log = logging.getLogger("wutherer.workers.analytics")


class AnalyticsAggregatorWorker:

    def __init__(self, bot: WuthererBot, interval_seconds: int = 300) -> None:
        self.bot = bot
        self.interval = interval_seconds
        self._task: asyncio.Task | None = None
        self._running = False

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run_loop(), name="wutherer-analytics-aggregator")
        log.info("Analytics Aggregator daemon started (interval=%ds)", self.interval)

    def stop(self) -> None:
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            log.info("Analytics Aggregator daemon stopped")

    async def _run_loop(self) -> None:
        await self.bot.wait_until_ready()
        while self._running:
            try:
                await self._collect_voice_telemetry()
            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error("Error in analytics aggregation cycle: %s", e, exc_info=True)

            try:
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                break

    async def _collect_voice_telemetry(self) -> None:
        if not self.bot.db_pool:
            return

        async with self.bot.db_pool.acquire() as db:
            analytics_dao = AnalyticsModel(db)
            interval_minutes = max(1, self.interval // 60)

            for guild in self.bot.guilds:
                active_voice_count = 0
                for vc in guild.voice_channels:

                    members = [m for m in vc.members if not m.bot and not m.voice.deaf and not m.voice.self_deaf]
                    active_voice_count += len(members)

                if active_voice_count > 0:
                    total_guild_voice_mins = active_voice_count * interval_minutes
                    await analytics_dao.record_voice_minutes(guild.id, total_guild_voice_mins)

