from __future__ import annotations
import datetime
import logging
import random
from typing import TYPE_CHECKING
import discord
from discord.ext import tasks

from database.models.giveaways import GiveawayModel

if TYPE_CHECKING:
    from core.bot import WuthererBot

log = logging.getLogger("wutherer.workers.giveaways")


class GiveawayCheckerWorker:

    def __init__(self, bot: WuthererBot):
        self.bot = bot
        self.check_loop.start()

    def stop(self):
        self.check_loop.cancel()

    @tasks.loop(seconds=15)
    async def check_loop(self):
        await self.bot.wait_until_ready()
        try:
            active = await GiveawayModel.get_active(self.bot.db)
            now = datetime.datetime.now(datetime.timezone.utc)
            for gw in active:
                try:
                    ends_at = datetime.datetime.fromisoformat(gw["ends_at"])
                    if ends_at.tzinfo is None:
                        ends_at = ends_at.replace(tzinfo=datetime.timezone.utc)

                    if now >= ends_at:
                        await GiveawayModel.end_giveaway(self.bot.db, gw["message_id"])
                        guild = self.bot.get_guild(gw["guild_id"])
                        if not guild:
                            continue
                        channel = guild.get_channel(gw["channel_id"])
                        if not channel:
                            continue

                        entries = gw["entries"]
                        winners_count = min(gw.get("winners", 1), len(entries))
                        if winners_count > 0:
                            winner_ids = random.sample(entries, winners_count)
                            winner_mentions = ", ".join(f"<@{uid}>" for uid in winner_ids)
                            embed = discord.Embed(
                                title="🎉 Giveaway Ended!",
                                description=f"**Prize:** {gw['prize']}\n**Winner(s):** {winner_mentions}\n**Host:** <@{gw['host_id']}>",
                                color=0x2ECC71,
                                timestamp=now
                            )
                            await channel.send(content=f"Congratulations {winner_mentions}!", embed=embed)
                        else:
                            embed = discord.Embed(
                                title="Giveaway Ended",
                                description=f"**Prize:** {gw['prize']}\nNo valid entries received.",
                                color=0x95A5A6
                            )
                            await channel.send(embed=embed)
                except Exception as ex:
                    log.debug("Error processing giveaway %s: %s", gw.get("id"), ex)
        except Exception as exc:
            log.error("Error in GiveawayCheckerWorker: %s", exc, exc_info=True)

