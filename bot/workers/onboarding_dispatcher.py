from __future__ import annotations
import asyncio
import logging
import time
from typing import Optional, NamedTuple
import discord

from database.models.onboarding import AdvancedWelcomeModel

log = logging.getLogger("wutherer.workers.onboarding")


class QueuedDelayedRole(NamedTuple):
    guild_id: int
    user_id: int
    role_ids: list[int]
    assign_at: float


class OnboardingDispatcherWorker:
    def __init__(self, bot, interval_seconds: int = 30):
        self.bot = bot
        self.interval = interval_seconds
        self._task: Optional[asyncio.Task] = None
        self._running = False
        self._queue: list[QueuedDelayedRole] = []

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        log.info("OnboardingDispatcherWorker started (interval: %ds)", self.interval)

    def stop(self) -> None:
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
        log.info("OnboardingDispatcherWorker stopped")

    def schedule_delayed_role(self, guild_id: int, user_id: int, role_ids: list[int], delay_minutes: int) -> None:
        target_time = time.time() + (delay_minutes * 60)
        self._queue.append(QueuedDelayedRole(guild_id, user_id, role_ids, target_time))

    async def _run_loop(self) -> None:
        await self.bot.wait_until_ready()
        while self._running:
            try:
                await self._process_queue()
            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error("Error in OnboardingDispatcherWorker loop: %s", e, exc_info=True)
            await asyncio.sleep(self.interval)

    async def _process_queue(self) -> None:
        now = time.time()
        ready = [item for item in self._queue if item.assign_at <= now]
        self._queue = [item for item in self._queue if item.assign_at > now]

        for item in ready:
            guild = self.bot.get_guild(item.guild_id)
            if not guild:
                continue

            member = guild.get_member(item.user_id)
            if not member:
                continue

            roles_to_add = []
            for rid in item.role_ids:
                r = guild.get_role(rid)
                if r and r not in member.roles:
                    roles_to_add.append(r)

            if roles_to_add:
                try:
                    await member.add_roles(*roles_to_add, reason="Wutherer Delayed Autorole Queue Worker")
                except Exception as err:
                    log.debug("Failed applying delayed roles to %s: %s", member.id, err)
