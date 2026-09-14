from __future__ import annotations
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_mod
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR
from services.youtube import YouTubeService
from database.models.youtube import YouTubeSubscription


class YouTube(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.yt = YouTubeService()

    @commands.group(name="youtube", aliases=["yt"], invoke_without_command=True)
    async def yt_group(self, ctx: commands.Context):
        await ctx.send_help(ctx.command)

    @yt_group.command(name="channel")
    async def channel_stats(self, ctx: commands.Context, *, query: str):
        async with ctx.typing():
            channels = await self.yt.search_channels(query, limit=1)
            if not channels:
                return await ctx.send(f"No YouTube channels found for `{query}`.")

            ch = channels[0]
            embed = discord.Embed(
                title=f"📺 {ch.get('title', 'YouTube Channel')}",
                description=(ch.get("description", "No description"))[:300],
                color=0xFF0000,
                url=f"https://youtube.com/channel/{ch.get('id')}"
            )
            if ch.get("thumbnail"):
                embed.set_thumbnail(url=ch["thumbnail"])

            stats = ch.get("statistics", {})
            subs = int(stats.get("subscriberCount", 0))
            views = int(stats.get("viewCount", 0))
            vids = int(stats.get("videoCount", 0))

            embed.add_field(name="Subscribers", value=f"**{subs:,}**", inline=True)
            embed.add_field(name="Total Views", value=f"**{views:,}**", inline=True)
            embed.add_field(name="Videos", value=f"**{vids:,}**", inline=True)
            await ctx.send(embed=embed)

    @yt_group.command(name="video", aliases=["search"])
    async def search_video(self, ctx: commands.Context, *, query: str):
        async with ctx.typing():
            videos = await self.yt.search_videos(query, limit=1)
            if not videos:
                return await ctx.send(f"No YouTube videos found matching `{query}`.")

            v = videos[0]
            v_url = f"https://www.youtube.com/watch?v={v['id']}"
            await ctx.send(f"🎬 **{v.get('title')}**\n{v_url}")

    @yt_group.command(name="subscribe", aliases=["sub", "notify"])
    @is_mod()
    async def subscribe_channel(
        self,
        ctx: commands.Context,
        channel_id_or_name: str,
        target_channel: Optional[discord.TextChannel] = None
    ):
        async with ctx.typing():
            chans = await self.yt.search_channels(channel_id_or_name, limit=1)
            if not chans:
                return await ctx.send("Could not find that YouTube channel.")

            ch = chans[0]
            c_id = ch["id"]
            c_name = ch.get("title", channel_id_or_name)
            notify_chan = target_channel or ctx.channel

            await YouTubeSubscription.add(
                self.bot.db, ctx.guild.id, c_id, c_name, notify_chan.id
            )
            await ctx.send(embed=discord.Embed(
                description=f"🔔 Subscribed to **{c_name}**! New uploads will be posted to {notify_chan.mention}.",
                color=BOT_COLOR_SUCCESS
            ))

    @yt_group.command(name="unsubscribe", aliases=["unsub"])
    @is_mod()
    async def unsubscribe_channel(self, ctx: commands.Context, channel_id_yt: str):
        await YouTubeSubscription.remove(self.bot.db, ctx.guild.id, channel_id_yt)
        await ctx.send(embed=discord.Embed(
            description=f"Unsubscribed from `{channel_id_yt}`.",
            color=BOT_COLOR_SUCCESS
        ))

    @yt_group.command(name="list")
    async def list_subscriptions(self, ctx: commands.Context):
        subs = await YouTubeSubscription.get_by_guild(self.bot.db, ctx.guild.id)
        if not subs:
            return await ctx.send("No active YouTube subscriptions in this server.")

        lines = []
        for s in subs:
            chan = ctx.guild.get_channel(s["notify_channel_id"])
            c_mention = chan.mention if chan else f"<#{s['notify_channel_id']}>"
            lines.append(f"• **{s['channel_name']}** (`{s['channel_id_yt']}`) ➔ {c_mention}")

        embed = discord.Embed(
            title=f"📺 YouTube Subscriptions ({len(subs)})",
            description="\n".join(lines),
            color=0xFF0000
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(YouTube(bot))

