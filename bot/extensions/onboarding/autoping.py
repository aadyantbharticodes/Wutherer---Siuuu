from __future__ import annotations
import discord
from discord.ext import commands
from typing import Optional

from database.models.onboarding import AutoPingModel
from services.onboarding_service import OnboardingService


class AutoPingCog(commands.Cog, name="Auto Ping"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="autoping", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def autoping_group(self, ctx: commands.Context):
        cfg = await AutoPingModel.get(self.bot.db, ctx.guild.id)
        embed = discord.Embed(
            title="🔔 Auto / Ghost Ping On Server Join",
            color=0x57F287 if cfg.get("enabled") else 0xED4245
        )
        embed.description = f"Status: **{'ENABLED' if cfg.get('enabled') else 'DISABLED'}**\nMode: **{cfg.get('ping_mode', 'ghost').upper()}**\nDelete Delay: **{cfg.get('delete_after_seconds', 5)}s**"

        ch_ids = cfg.get("channels", [])
        ch_mentions = [f"<#{cid}>" for cid in ch_ids] if ch_ids else ["*None*"]
        embed.add_field(name="Target Channels", value=", ".join(ch_mentions), inline=False)
        embed.add_field(name="Message Template", value=f"```\n{cfg.get('message_template', 'Welcome {user.mention} to {guild.name}!')}\n```", inline=False)
        embed.add_field(name="Commands", value=(
            "`s!autoping toggle` — Enable/disable Auto Ping\n"
            "`s!autoping channel add/remove <#channel>` — Manage ping channels\n"
            "`s!autoping mode <ghost/persistent>` — Set ping style\n"
            "`s!autoping delay <seconds>` — Ghost delete delay (0-60s)\n"
            "`s!autoping message <template>` — Set custom ping text\n"
            "`s!autoping test` — Trigger test ping in target channels"
        ), inline=False)
        embed.set_footer(text="Ghost mode automatically deletes the ping to attract attention without chat clutter")
        await ctx.send(embed=embed)

    @autoping_group.command(name="toggle")
    @commands.has_permissions(manage_guild=True)
    async def autoping_toggle(self, ctx: commands.Context):
        cfg = await AutoPingModel.get(self.bot.db, ctx.guild.id)
        new_state = 0 if cfg.get("enabled") else 1
        await AutoPingModel.update(self.bot.db, ctx.guild.id, enabled=new_state)
        await ctx.send(f"🔔 Auto Ping on join is now **{'ENABLED' if new_state else 'DISABLED'}**.")

    @autoping_group.group(name="channel", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def autoping_channel(self, ctx: commands.Context):
        await ctx.send("Usage: `s!autoping channel add <#channel>` or `s!autoping channel remove <#channel>`")

    @autoping_channel.command(name="add")
    @commands.has_permissions(manage_guild=True)
    async def autoping_channel_add(self, ctx: commands.Context, channel: discord.TextChannel):
        cfg = await AutoPingModel.get(self.bot.db, ctx.guild.id)
        channels = cfg.get("channels", [])
        if channel.id in channels:
            await ctx.send(f"ℹ️ {channel.mention} is already an Auto Ping target.")
            return
        channels.append(channel.id)
        await AutoPingModel.update(self.bot.db, ctx.guild.id, channels=channels)
        await ctx.send(f"✅ Added {channel.mention} to Auto Ping targets.")

    @autoping_channel.command(name="remove")
    @commands.has_permissions(manage_guild=True)
    async def autoping_channel_remove(self, ctx: commands.Context, channel: discord.TextChannel):
        cfg = await AutoPingModel.get(self.bot.db, ctx.guild.id)
        channels = cfg.get("channels", [])
        if channel.id not in channels:
            await ctx.send(f"ℹ️ {channel.mention} is not in the Auto Ping list.")
            return
        channels.remove(channel.id)
        await AutoPingModel.update(self.bot.db, ctx.guild.id, channels=channels)
        await ctx.send(f"🗑️ Removed {channel.mention} from Auto Ping targets.")

    @autoping_group.command(name="mode")
    @commands.has_permissions(manage_guild=True)
    async def autoping_mode(self, ctx: commands.Context, mode: str):
        m = mode.lower()
        if m not in ("ghost", "persistent"):
            await ctx.send("❌ Mode must be either `ghost` (auto-delete) or `persistent` (stays in chat).")
            return
        await AutoPingModel.update(self.bot.db, ctx.guild.id, ping_mode=m)
        await ctx.send(f"🎯 Auto Ping mode updated to **{m.upper()}**.")

    @autoping_group.command(name="delay")
    @commands.has_permissions(manage_guild=True)
    async def autoping_delay(self, ctx: commands.Context, seconds: int):
        sec = max(1, min(seconds, 60))
        await AutoPingModel.update(self.bot.db, ctx.guild.id, delete_after_seconds=sec)
        await ctx.send(f"⏱️ Ghost Ping delete delay set to **{sec}** seconds.")

    @autoping_group.command(name="message")
    @commands.has_permissions(manage_guild=True)
    async def autoping_message(self, ctx: commands.Context, *, text: str):
        await AutoPingModel.update(self.bot.db, ctx.guild.id, message_template=text)
        await ctx.send("✅ Auto Ping message template updated!")

    @autoping_group.command(name="test")
    @commands.has_permissions(manage_guild=True)
    async def autoping_test(self, ctx: commands.Context):
        await OnboardingService.dispatch_auto_ping(self.bot, self.bot.db, ctx.author)
        await ctx.send("🔔 Dispatched test ping to configured target channels.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        await OnboardingService.dispatch_auto_ping(self.bot, self.bot.db, member)


async def setup(bot):
    await bot.add_cog(AutoPingCog(bot))
