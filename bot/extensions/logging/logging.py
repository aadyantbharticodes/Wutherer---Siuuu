from __future__ import annotations
import datetime
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_admin
from config import BOT_COLOR, BOT_COLOR_WARNING, BOT_COLOR_ERROR, BOT_COLOR_SUCCESS
from database.models.logging import LoggingConfigModel


class Logging(WuthererCog):

    @commands.group(name="logging", aliases=["auditlog"], invoke_without_command=True)
    @is_admin()
    async def logging_group(self, ctx: commands.Context):
        cfg = await LoggingConfigModel.get(self.bot.db, ctx.guild.id)
        chan = ctx.guild.get_channel(cfg.get("channel_id")) if cfg.get("channel_id") else None
        embed = discord.Embed(
            title="📋 Audit Logging Status",
            color=BOT_COLOR
        )
        embed.add_field(name="Status", value="Enabled" if cfg.get("enabled") else "Disabled", inline=True)
        embed.add_field(name="Log Channel", value=chan.mention if chan else "None", inline=True)
        embed.add_field(
            name="Events Tracked",
            value=(
                f"• Message Deletes: {'✅' if cfg.get('message_delete') else '❌'}\n"
                f"• Message Edits: {'✅' if cfg.get('message_edit') else '❌'}\n"
                f"• Member Joins: {'✅' if cfg.get('member_join') else '❌'}\n"
                f"• Member Leaves: {'✅' if cfg.get('member_leave') else '❌'}\n"
                f"• Channel Changes: {'✅' if cfg.get('channel_changes') else '❌'}\n"
                f"• Role Changes: {'✅' if cfg.get('role_changes') else '❌'}"
            ),
            inline=False
        )
        await ctx.send(embed=embed)

    @logging_group.command(name="channel")
    @is_admin()
    async def set_logging_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        await LoggingConfigModel.update(self.bot.db, ctx.guild.id, enabled=1, channel_id=channel.id)
        await ctx.send(embed=discord.Embed(
            description=f"Audit logs will now be sent to {channel.mention}.",
            color=BOT_COLOR_SUCCESS
        ))

    @logging_group.command(name="disable")
    @is_admin()
    async def disable_logging(self, ctx: commands.Context):
        await LoggingConfigModel.update(self.bot.db, ctx.guild.id, enabled=0)
        await ctx.send(embed=discord.Embed(
            description="Audit logging has been disabled.",
            color=BOT_COLOR_SUCCESS
        ))

    async def _get_log_channel(self, guild: discord.Guild, event_key: str) -> Optional[discord.TextChannel]:
        cfg = await LoggingConfigModel.get(self.bot.db, guild.id)
        if not cfg.get("enabled") or not cfg.get(event_key, 1):
            return None
        chan_id = cfg.get("channel_id")
        if not chan_id:
            return None
        channel = guild.get_channel(chan_id)
        if channel and channel.permissions_for(guild.me).send_messages:
            return channel
        return None

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if not message.guild or message.author.bot:
            return
        log_channel = await self._get_log_channel(message.guild, "message_delete")
        if not log_channel or log_channel.id == message.channel.id:
            return

        embed = discord.Embed(
            title="🗑️ Message Deleted",
            color=BOT_COLOR_ERROR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Author", value=f"{message.author.mention} (`{message.author.id}`)", inline=True)
        content = message.content or "*No text content (may have contained embed or attachment)*"
        embed.add_field(name="Content", value=content[:1020], inline=False)
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if not before.guild or before.author.bot or before.content == after.content:
            return
        log_channel = await self._get_log_channel(before.guild, "message_edit")
        if not log_channel:
            return

        embed = discord.Embed(
            title="✏️ Message Edited",
            color=BOT_COLOR_WARNING,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_author(name=str(before.author), icon_url=before.author.display_avatar.url)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        embed.add_field(name="Jump Link", value=f"[Jump to Message]({after.jump_url})", inline=True)
        embed.add_field(name="Before", value=(before.content or "*None*")[:1000], inline=False)
        embed.add_field(name="After", value=(after.content or "*None*")[:1000], inline=False)
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        log_channel = await self._get_log_channel(channel.guild, "channel_changes")
        if not log_channel:
            return
        embed = discord.Embed(
            title="📁 Channel Created",
            description=f"Channel {channel.mention} (`{channel.name}`) was created.",
            color=BOT_COLOR_SUCCESS,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        log_channel = await self._get_log_channel(channel.guild, "channel_changes")
        if not log_channel:
            return
        embed = discord.Embed(
            title="📁 Channel Deleted",
            description=f"Channel **#{channel.name}** (`{channel.id}`) was deleted.",
            color=BOT_COLOR_ERROR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException:
            pass


async def setup(bot):
    await bot.add_cog(Logging(bot))

