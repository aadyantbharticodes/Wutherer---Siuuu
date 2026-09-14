from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from discord.ext import commands

from config import BOT_COLOR

if TYPE_CHECKING:
    from core.bot import WuthererBot


class WuthererCog(commands.Cog):

    def __init__(self, bot: WuthererBot):
        self.bot = bot
        self.log = logging.getLogger(f"sentinel.{self.qualified_name}")

    @property
    def db(self):
        return self.bot.db

    @property
    def session(self):
        return self.bot.session

    @property
    def color(self):
        return BOT_COLOR

