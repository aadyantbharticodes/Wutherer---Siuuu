from __future__ import annotations

import time
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from bot.core.cog import WuthererCog
from bot.core.context import WuthererContext
from bot.core.checks import is_mod
from bot.database.models.analytics import AnalyticsModel

if TYPE_CHECKING:
    from bot.core.bot import WuthererBot


class Analytics(WuthererCog, name="Analytics"):

    def __init__(self, bot: WuthererBot) -> None:
        super().__init__(bot)

    @WuthererCog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not message.guild:
            return

        if self.bot.db_pool:
            try:
                async with self.bot.db_pool.acquire() as db:
                    dao = AnalyticsModel(db)
                    await dao.record_message_activity(message.guild.id, message.channel.id, message.author.id)
            except Exception:
                pass

    @WuthererCog.listener()
    async def on_command_completion(self, ctx: commands.Context) -> None:
        if not ctx.guild:
            return

        if self.bot.db_pool:
            try:
                async with self.bot.db_pool.acquire() as db:
                    dao = AnalyticsModel(db)
                    await dao.record_command_activity(ctx.guild.id)
            except Exception:
                pass

    @commands.group(name="stats", aliases=["telemetry", "metrics"], invoke_without_command=True)
    async def stats_group(self, ctx: WuthererContext) -> None:
        await self.stats_overview(ctx)

    @stats_group.command(name="overview", aliases=["summary"])
    async def stats_overview(self, ctx: WuthererContext) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = AnalyticsModel(db)
            totals = await dao.get_overview_totals(ctx.guild.id)
            recent_24h = await dao.get_recent_hourly(ctx.guild.id, hours=24)

        messages_24h = sum(r.message_count for r in recent_24h)
        voice_24h = sum(r.voice_minutes for r in recent_24h)
        commands_24h = sum(r.commands_run for r in recent_24h)

        embed = self.bot.embed.create(
            title=f"📊 Server Intelligence & Activity — {ctx.guild.name}",
            description="Real-time telemetry and engagement analysis recorded by Sentinel.",
        )

        embed.add_field(
            name="Past 24 Hours",
            value=(
                f"• **Messages Sent:** `{messages_24h:,}`\n"
                f"• **Voice Time:** `{voice_24h:,} mins`\n"
                f"• **Commands Run:** `{commands_24h:,}`\n"
            ),
            inline=True,
        )

        embed.add_field(
            name="All-Time Recorded",
            value=(
                f"• **Total Messages:** `{totals['total_messages']:,}`\n"
                f"• **Total Voice:** `{totals['total_voice_minutes']:,} mins`\n"
                f"• **Total Commands:** `{totals['total_commands']:,}`\n"
            ),
            inline=True,
        )


        online_members = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
        embed.add_field(
            name="Current Population",
            value=(
                f"• **Total Members:** `{ctx.guild.member_count:,}`\n"
                f"• **Online Now:** `{online_members:,}`\n"
                f"• **Text Channels:** `{len(ctx.guild.text_channels)}`\n"
                f"• **Voice Channels:** `{len(ctx.guild.voice_channels)}`\n"
            ),
            inline=False,
        )

        await ctx.send(embed=embed)

    @stats_group.command(name="channels", aliases=["topchannels"])
    async def stats_channels(self, ctx: WuthererContext) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = AnalyticsModel(db)
            top = await dao.get_top_channels(ctx.guild.id, limit=10)

        if not top:
            await ctx.send_warn("No channel telemetry recorded yet. Chatter will populate here shortly!")
            return

        embed = self.bot.embed.create(
            title=f"🏆 Top Active Channels — {ctx.guild.name}",
            description="Channels ranked by historical message volume.",
        )

        lines = []
        for i, ch_stat in enumerate(top, 1):
            ch = ctx.guild.get_channel(ch_stat.channel_id)
            name = ch.mention if ch else f"Deleted Channel (`{ch_stat.channel_id}`)"
            lines.append(f"`#{i:02d}` {name} — **`{ch_stat.message_count:,}` messages**")

        embed.description = "\n".join(lines)
        await ctx.send(embed=embed)

    @stats_group.command(name="heatmap", aliases=["activity"])
    async def stats_heatmap(self, ctx: WuthererContext) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = AnalyticsModel(db)
            records = await dao.get_recent_hourly(ctx.guild.id, hours=24)

        if not records:
            await ctx.send_warn("Telemetry data is building up. Check back in an hour!")
            return


        max_msgs = max((r.message_count for r in records), default=1)
        if max_msgs == 0:
            max_msgs = 1

        chart_bars = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        chart_str = ""

        for r in records:
            fraction = r.message_count / max_msgs
            bar_idx = min(len(chart_bars) - 1, int(fraction * (len(chart_bars) - 1)))
            chart_str += chart_bars[bar_idx]

        total_msgs = sum(r.message_count for r in records)
        peak_hour = max(records, key=lambda r: r.message_count)
        peak_time_str = f"<t:{peak_hour.timestamp_hour}:t>"

        embed = self.bot.embed.create(
            title=f"📈 24-Hour Chatter Curve — {ctx.guild.name}",
            description=(
                f"**24h Volume Curve:**\n```\n{chart_str}\n(24h ago) ───────────────► (Now)\n```\n"
                f"• **Peak Velocity:** `{peak_hour.message_count:,} msgs/hr` at {peak_time_str}\n"
                f"• **Average Velocity:** `{total_msgs // max(1, len(records)):,} msgs/hr`\n"
                f"• **Total Past 24h:** `{total_msgs:,} messages`\n"
            ),
        )
        await ctx.send(embed=embed)

    @commands.command(name="insights")
    @is_mod()
    async def insights_cmd(self, ctx: WuthererContext) -> None:
        guild = ctx.guild
        bots_count = sum(1 for m in guild.members if m.bot)
        humans_count = guild.member_count - bots_count
        bot_ratio = (bots_count / max(1, guild.member_count)) * 100

        embed = self.bot.embed.create(
            title=f"🔍 Server Insights & Health Audit — {guild.name}",
            description="Holistic configuration and demographic review.",
        )

        embed.add_field(
            name="Demographics",
            value=(
                f"• **Humans:** `{humans_count:,}`\n"
                f"• **Bots:** `{bots_count:,}` ({bot_ratio:.1f}%)\n"
                f"• **Roles:** `{len(guild.roles)}`\n"
            ),
            inline=True,
        )

        embed.add_field(
            name="Features & Level",
            value=(
                f"• **Boost Level:** `Tier {guild.premium_tier}`\n"
                f"• **Total Boosts:** `{guild.premium_subscription_count}`\n"
                f"• **2FA Mod Level:** `{'Enabled' if guild.mfa_level else 'Disabled'}`\n"
            ),
            inline=True,
        )

        await ctx.send(embed=embed)


async def setup(bot: WuthererBot) -> None:
    await bot.add_cog(Analytics(bot))

