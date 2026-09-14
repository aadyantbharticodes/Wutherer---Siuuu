from __future__ import annotations
import asyncio
import logging
import time
from typing import Optional
import discord

from database.models.antinuke import AntiNukeModel
from services.antinuke import AntiNukeService

log = logging.getLogger("wutherer.workers.antinuke")


class AntiNukeWatchdogWorker:
    def __init__(self, bot, interval_seconds: int = 15):
        self.bot = bot
        self.interval = interval_seconds
        self._task: Optional[asyncio.Task] = None
        self._running = False
        self.service = AntiNukeService(bot, bot.db)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        log.info("AntiNukeWatchdogWorker started (interval: %ds)", self.interval)

    def stop(self) -> None:
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
        log.info("AntiNukeWatchdogWorker stopped")

    async def _run_loop(self) -> None:
        await self.bot.wait_until_ready()
        while self._running:
            try:
                await self._audit_active_guilds()
            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error("Error in AntiNukeWatchdogWorker loop: %s", e, exc_info=True)
            await asyncio.sleep(self.interval)

    async def _audit_active_guilds(self) -> None:
        for guild in self.bot.guilds:
            try:
                cfg = await AntiNukeModel.get_config(self.bot.db, guild.id)
                if not cfg.get("enabled"):
                    continue

                if not guild.me.guild_permissions.view_audit_log:
                    continue

                recent_time = time.time() - self.interval
                async for entry in guild.audit_logs(limit=10):
                    if entry.created_at.timestamp() < recent_time:
                        break

                    if entry.action == discord.AuditLogAction.bot_add and entry.target and entry.target.bot:
                        culprit = entry.user
                        if culprit and culprit.id != guild.owner_id and culprit.id != self.bot.user.id:
                            is_wl = await AntiNukeModel.is_whitelisted(self.bot.db, guild.id, culprit.id)
                            if not is_wl:
                                await self.service.punish_culprit(
                                    guild,
                                    culprit.id,
                                    "unauthorized_bot_add",
                                    1,
                                    cfg.get("action_type", "ban")
                                )
            except Exception as guild_err:
                log.debug("Failed auditing guild %s: %s", guild.id, guild_err)
