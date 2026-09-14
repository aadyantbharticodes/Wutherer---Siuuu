from __future__ import annotations
import datetime
import logging
from typing import TYPE_CHECKING
import discord
from discord.ext import tasks

if TYPE_CHECKING:
    from core.bot import WuthererBot

log = logging.getLogger("wutherer.workers.reminders")


class ReminderDispatcherWorker:

    def __init__(self, bot: WuthererBot):
        self.bot = bot
        self.check_loop.start()

    def stop(self):
        self.check_loop.cancel()

    @tasks.loop(seconds=15)
    async def check_loop(self):
        await self.bot.wait_until_ready()
        try:
            rows = await self.bot.db.fetch(
                "SELECT * FROM reminders WHERE remind_at <= datetime('now')"
            )
            for r in rows:
                try:
                    user = self.bot.get_user(r["user_id"]) or await self.bot.fetch_user(r["user_id"])
                    embed = discord.Embed(
                        title="⏰ Reminder!",
                        description=f"You asked to be reminded:\n\n> {r['message']}",
                        color=0x6C5CE7,
                        timestamp=datetime.datetime.now(datetime.timezone.utc)
                    )
                    sent = False
                    if user:
                        try:
                            await user.send(embed=embed)
                            sent = True
                        except discord.HTTPException:
                            pass

                    if not sent and r.get("guild_id") and r.get("channel_id"):
                        guild = self.bot.get_guild(r["guild_id"])
                        if guild:
                            channel = guild.get_channel(r["channel_id"])
                            if channel:
                                await channel.send(content=f"<@{r['user_id']}>", embed=embed)

                    await self.bot.db.execute("DELETE FROM reminders WHERE id = ?", r["id"])
                except Exception as ex:
                    log.debug("Error dispatching reminder %s: %s", r.get("id"), ex)
        except Exception as exc:
            log.error("Error in ReminderDispatcherWorker: %s", exc, exc_info=True)

