from __future__ import annotations
import logging
from typing import TYPE_CHECKING
import discord
from discord.ext import tasks

if TYPE_CHECKING:
    from core.bot import WuthererBot

log = logging.getLogger("wutherer.workers.scheduled")


class ScheduledMessagesWorker:

    def __init__(self, bot: WuthererBot):
        self.bot = bot
        self.check_loop.start()

    def stop(self):
        self.check_loop.cancel()

    @tasks.loop(minutes=1)
    async def check_loop(self):
        await self.bot.wait_until_ready()


