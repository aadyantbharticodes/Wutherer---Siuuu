from __future__ import annotations
import asyncio
import logging
from typing import TYPE_CHECKING
import discord
from discord.ext import tasks

from database.models.youtube import YouTubeSubscription
from services.youtube import YouTubeService

if TYPE_CHECKING:
    from core.bot import WuthererBot

log = logging.getLogger("wutherer.workers.youtube")


class YouTubeMonitorWorker:

    def __init__(self, bot: WuthererBot):
        self.bot = bot
        self.yt = YouTubeService()
        self.check_loop.start()

    def stop(self):
        self.check_loop.cancel()

    @tasks.loop(minutes=5)
    async def check_loop(self):
        await self.bot.wait_until_ready()
        try:
            subs = await YouTubeSubscription.get_all_active(self.bot.db)
            for sub in subs:
                try:
                    vids = await self.yt.get_channel_videos(sub["channel_id_yt"], limit=1)
                    if not vids:
                        continue
                    latest = vids[0]
                    vid_id = latest.get("id")
                    if not vid_id:
                        continue


                    if sub.get("last_video_id") != vid_id:
                        await YouTubeSubscription.update_last_video(self.bot.db, sub["id"], vid_id)
                        if sub.get("last_video_id") is not None:
                            guild = self.bot.get_guild(sub["guild_id"])
                            if guild:
                                channel = guild.get_channel(sub["notify_channel_id"])
                                if channel and channel.permissions_for(guild.me).send_messages:
                                    role_ping = f"<@&{sub['notify_role_id']}> " if sub.get("notify_role_id") else ""
                                    title = latest.get("title", "New Video")
                                    url = f"https://www.youtube.com/watch?v={vid_id}"
                                    msg = sub.get("custom_message") or "{role}**{channel}** uploaded a new video: **{title}**!\n{url}"
                                    msg = msg.replace("{role}", role_ping)
                                    msg = msg.replace("{channel}", sub.get("channel_name", "YouTube"))
                                    msg = msg.replace("{title}", title)
                                    msg = msg.replace("{url}", url)
                                    await channel.send(msg)
                except Exception as ex:
                    log.debug("Error checking YouTube channel %s: %s", sub.get("channel_id_yt"), ex)
        except Exception as exc:
            log.error("Error in YouTubeMonitorWorker loop: %s", exc, exc_info=True)

