from __future__ import annotations
import asyncio
import logging
import time
from typing import Optional

import aiohttp
import discord
from discord.ext import commands, tasks

from config import (
    TOKEN, BOT_NAME, DEFAULT_PREFIX, BOT_COLOR, OWNER_IDS,
    API_ENABLED, API_PORT,
)
from database.pool import DatabasePool

log = logging.getLogger("Wutherer")


class WuthererBot(commands.AutoShardedBot):
    db: DatabasePool
    session: aiohttp.ClientSession
    uptime_start: float

    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=self._resolve_prefix,
            case_insensitive=True,
            intents=intents,
            status=discord.Status.online,
            strip_after_prefix=True,
            owner_ids=set(OWNER_IDS),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, replied_user=False, roles=False
            ),
            shard_count=1,
        )
        self._status_idx = 0
        self.db = DatabasePool()
        self.db_pool = self.db
        self.uptime_start = time.time()
        self.color = BOT_COLOR

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.db.initialize()
        await self._load_extensions()
        self._rotate_status.start()
        self._start_workers()

    def _start_workers(self):
        from workers import (
            YouTubeMonitorWorker,
            GiveawayCheckerWorker,
            ReminderDispatcherWorker,
            MinecraftStatusUpdaterWorker,
            AnalyticsAggregatorWorker,
            AntiNukeWatchdogWorker,
            OnboardingDispatcherWorker,
        )
        self.workers = [
            YouTubeMonitorWorker(self),
            GiveawayCheckerWorker(self),
            ReminderDispatcherWorker(self),
            MinecraftStatusUpdaterWorker(self),
            AnalyticsAggregatorWorker(self),
            AntiNukeWatchdogWorker(self),
            OnboardingDispatcherWorker(self),
        ]
        for w in self.workers:
            w.start()

    async def close(self):
        self._rotate_status.cancel()
        if hasattr(self, "workers"):
            for w in self.workers:
                try:
                    w.stop()
                except Exception:
                    pass
        await self.session.close()
        await self.db.close()
        await super().close()


    async def _load_extensions(self):
        from config import BASE_DIR
        loaded, failed = 0, 0

        ext_root = BASE_DIR / "extensions"
        if not ext_root.is_dir():
            log.warning("Extensions directory not found at %s", ext_root)
            return

        for category_dir in sorted(ext_root.iterdir()):
            if not category_dir.is_dir() or category_dir.name.startswith("_"):
                continue
            for py_file in sorted(category_dir.glob("*.py")):
                if py_file.name.startswith("_"):
                    continue
                ext_path = f"extensions.{category_dir.name}.{py_file.stem}"
                try:
                    await self.load_extension(ext_path)
                    loaded += 1
                except Exception as exc:
                    failed += 1
                    log.error("Failed to load %s: %s", ext_path, exc, exc_info=True)

        try:
            await self.load_extension("jishaku")
            loaded += 1
        except Exception:
            log.debug("jishaku not available")

        log.info("Loaded %d extensions (%d failed)", loaded, failed)

    async def _resolve_prefix(self, bot: commands.Bot, message: discord.Message):
        if not message.guild:
            return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)

        from database.models.guild import GuildSettings
        settings = await GuildSettings.get(self.db, message.guild.id)
        prefix = settings.get("prefix", DEFAULT_PREFIX)

        from database.models.user import UserSettings
        noprefix = await UserSettings.has_noprefix(self.db, message.author.id)
        if noprefix:
            return commands.when_mentioned_or(prefix, "")(bot, message)
        return commands.when_mentioned_or(prefix)(bot, message)

    @tasks.loop(seconds=30)
    async def _rotate_status(self):
        await self.wait_until_ready()
        if not self.guilds:
            return

        users = sum(g.member_count or 0 for g in self.guilds)
        guilds = len(self.guilds)

        statuses = [
            (discord.ActivityType.watching, f"{guilds:,} servers"),
            (discord.ActivityType.watching, f"{users:,} users"),
            (discord.ActivityType.playing, f"{DEFAULT_PREFIX}help"),
            (discord.ActivityType.listening, "your commands"),
        ]

        activity_type, name = statuses[self._status_idx % len(statuses)]
        await self.change_presence(
            activity=discord.Activity(type=activity_type, name=name)
        )
        self._status_idx += 1

    async def get_context(self, origin: discord.Message | discord.Interaction, *, cls=None):
        from core.context import Context
        return await super().get_context(origin, cls=cls or Context)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return
        if after.author.bot or not after.guild:
            return
        ctx = await self.get_context(after)
        if ctx.command:
            await self.invoke(ctx)

    def embed(self, description: str = None, **kwargs) -> discord.Embed:
        return discord.Embed(color=self.color, description=description, **kwargs)


