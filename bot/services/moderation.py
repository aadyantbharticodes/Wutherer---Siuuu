from __future__ import annotations
import datetime
from typing import Optional, Union
import discord

from config import BOT_NAME, BOT_COLOR_ERROR, BOT_COLOR_WARNING
from database.pool import DatabasePool
from database.models.moderation import ModCases, Warnings
from database.models.guild import GuildSettings


class ModerationService:

    @staticmethod
    async def send_punishment_dm(
        member: discord.Member,
        action: str,
        reason: Optional[str] = None,
        duration: Optional[str] = None
    ) -> bool:
        try:
            desc = f"You have received a **{action.upper()}** in **{member.guild.name}**."
            if reason:
                desc += f"\n**Reason:** {reason}"
            if duration:
                desc += f"\n**Duration:** {duration}"
            embed = discord.Embed(
                title=f"{action.capitalize()} Notice",
                description=desc,
                color=BOT_COLOR_ERROR,
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_footer(text=f"{BOT_NAME} Security")
            await member.send(embed=embed)
            return True
        except (discord.Forbidden, discord.HTTPException):
            return False

    @staticmethod
    async def log_mod_case(
        bot,
        guild: discord.Guild,
        moderator: Union[discord.Member, discord.User],
        target: Union[discord.Member, discord.User],
        action: str,
        reason: Optional[str] = None,
        duration: Optional[int] = None
    ) -> int:
        case_id = await ModCases.create(
            bot.db, guild.id, target.id, moderator.id, action, reason, duration
        )

        settings = await GuildSettings.get(bot.db, guild.id)
        log_channel_id = settings.get("mod_log_channel_id") or settings.get("log_channel_id")
        if log_channel_id:
            channel = guild.get_channel(log_channel_id)
            if channel and channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title=f"Mod Case #{case_id} | {action.upper()}",
                    color=BOT_COLOR_WARNING if action in ("warn", "timeout") else BOT_COLOR_ERROR,
                    timestamp=datetime.datetime.now(datetime.timezone.utc)
                )
                embed.add_field(name="Target", value=f"{target} (`{target.id}`)", inline=True)
                embed.add_field(name="Moderator", value=f"{moderator} (`{moderator.id}`)", inline=True)
                if duration:
                    embed.add_field(name="Duration", value=f"{duration}s", inline=True)
                embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
                embed.set_footer(text=f"{BOT_NAME} Case Tracking")
                try:
                    await channel.send(embed=embed)
                except discord.HTTPException:
                    pass
        return case_id

