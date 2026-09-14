from __future__ import annotations
import logging
from typing import TYPE_CHECKING
import discord
from discord.ext import tasks

from database.models.minecraft import MinecraftServerModel
from services.minecraft import MinecraftService

if TYPE_CHECKING:
    from core.bot import WuthererBot

log = logging.getLogger("wutherer.workers.minecraft")


class MinecraftStatusUpdaterWorker:

    def __init__(self, bot: WuthererBot):
        self.bot = bot
        self.mc = MinecraftService()
        self.update_loop.start()

    def stop(self):
        self.update_loop.cancel()

    @tasks.loop(minutes=2)
    async def update_loop(self):
        await self.bot.wait_until_ready()
        try:
            servers = await MinecraftServerModel.get_all(self.bot.db)
            for s in servers:
                try:
                    guild = self.bot.get_guild(s["guild_id"])
                    if not guild:
                        continue
                    channel = guild.get_channel(s["channel_id"])
                    if not channel or not channel.permissions_for(guild.me).send_messages:
                        continue

                    status = await self.mc.get_server_status(s["server_ip"], server_type=s.get("server_type", "java"))
                    online = status.get("online", False) if status else False

                    if online:
                        motd = status.get("motd", {}).get("clean", "")
                        if isinstance(motd, list):
                            motd = "\n".join(motd)
                        players = status.get("players", {})
                        embed = discord.Embed(
                            title=f"🟢 {s['server_ip']} (Online)",
                            description=f"```\n{motd}\n```" if motd else "Server online",
                            color=0x2ECC71,
                            timestamp=discord.utils.utcnow()
                        )
                        embed.add_field(name="Players", value=f"{players.get('online', 0)} / {players.get('max', 0)}", inline=True)
                        embed.add_field(name="Version", value=status.get("version", "Unknown"), inline=True)
                    else:
                        embed = discord.Embed(
                            title=f"🔴 {s['server_ip']} (Offline)",
                            description="Server could not be reached.",
                            color=0xE74C3C,
                            timestamp=discord.utils.utcnow()
                        )

                    msg_id = s.get("message_id")
                    if msg_id:
                        try:
                            msg = await channel.fetch_message(msg_id)
                            await msg.edit(embed=embed)
                            continue
                        except (discord.NotFound, discord.HTTPException):
                            pass

                    new_msg = await channel.send(embed=embed)
                    await MinecraftServerModel.update_message_id(self.bot.db, s["id"], new_msg.id)
                except Exception as ex:
                    log.debug("Error updating Minecraft server %s: %s", s.get("server_ip"), ex)
        except Exception as exc:
            log.error("Error in MinecraftStatusUpdaterWorker: %s", exc, exc_info=True)

