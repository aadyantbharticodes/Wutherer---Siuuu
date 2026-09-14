from __future__ import annotations
import datetime
import os
import platform
import time
from typing import Optional, Union

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_NAME, BOT_COLOR, BOT_COLOR_SUCCESS, DEFAULT_PREFIX


class Utility(WuthererCog):

    @commands.command(name="ping", aliases=["latency"])
    async def check_ping(self, ctx: commands.Context):
        ws_ping = round(self.bot.latency * 1000)

        t1 = time.perf_counter()
        await self.bot.db.fetchval("SELECT 1")
        db_ping = round((time.perf_counter() - t1) * 1000, 1)

        embed = discord.Embed(title="🏓 Pong!", color=BOT_COLOR)
        embed.add_field(name="WebSocket Latency", value=f"`{ws_ping}ms`", inline=True)
        embed.add_field(name="Database Latency", value=f"`{db_ping}ms`", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="uptime")
    async def view_uptime(self, ctx: commands.Context):
        diff = int(time.time() - self.bot.uptime_start)
        days, rem = divmod(diff, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"

        embed = discord.Embed(
            title="⏱️ Uptime",
            description=f"Sentinel has been continuously online for:\n**{uptime_str}**",
            color=BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="botinfo", aliases=["about", "info"])
    async def bot_info(self, ctx: commands.Context):
        total_guilds = len(self.bot.guilds)
        total_users = sum(g.member_count or 0 for g in self.bot.guilds)
        total_channels = sum(len(g.channels) for g in self.bot.guilds)

        embed = discord.Embed(
            title=f"🤖 {BOT_NAME} Information",
            description=f"Next-generation modular Discord platform with automated intelligence.",
            color=BOT_COLOR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Servers", value=f"{total_guilds:,}", inline=True)
        embed.add_field(name="Users", value=f"{total_users:,}", inline=True)
        embed.add_field(name="Channels", value=f"{total_channels:,}", inline=True)
        embed.add_field(name="discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="Platform", value=platform.system(), inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["whois", "user", "ui"])
    async def user_info(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        target = member or ctx.author
        roles = [r.mention for r in reversed(target.roles) if not r.is_default()]

        embed = discord.Embed(
            title=f"User Info — {target.display_name}",
            color=target.color if target.color.value != 0 else BOT_COLOR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Tag / Name", value=f"`{target}`", inline=True)
        embed.add_field(name="ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="Bot?", value="Yes" if target.bot else "No", inline=True)
        embed.add_field(name="Account Created", value=f"<t:{int(target.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Joined Server", value=f"<t:{int(target.joined_at.timestamp())}:R>" if target.joined_at else "Unknown", inline=True)
        embed.add_field(name="Top Role", value=target.top_role.mention, inline=True)
        if roles:
            roles_str = ", ".join(roles[:10]) + (f" +{len(roles)-10} more" if len(roles) > 10 else "")
            embed.add_field(name=f"Roles ({len(roles)})", value=roles_str, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["guildinfo", "si"])
    async def server_info(self, ctx: commands.Context):
        guild = ctx.guild
        owner = guild.owner or await self.bot.fetch_user(guild.owner_id)

        embed = discord.Embed(
            title=f"Server Info — {guild.name}",
            color=BOT_COLOR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.add_field(name="Owner", value=f"{owner.mention} (`{owner.id}`)", inline=True)
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="Created", value=f"<t:{int(guild.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Total Members", value=f"**{guild.member_count:,}**", inline=True)
        embed.add_field(name="Text Channels", value=f"**{len(guild.text_channels)}**", inline=True)
        embed.add_field(name="Voice Channels", value=f"**{len(guild.voice_channels)}**", inline=True)
        embed.add_field(name="Roles", value=f"**{len(guild.roles)}**", inline=True)
        embed.add_field(name="Emojis", value=f"**{len(guild.emojis)}**", inline=True)
        embed.add_field(name="Boost Level", value=f"Tier **{guild.premium_tier}** ({guild.premium_subscription_count} boosts)", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="avatar", aliases=["av", "pfp"])
    async def view_avatar(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]] = None):
        target = user or ctx.author
        url = target.display_avatar.with_size(1024).url
        embed = discord.Embed(title=f"Avatar for {target.display_name}", color=BOT_COLOR)
        embed.set_image(url=url)
        embed.add_field(name="Links", value=f"[Direct Link]({url})")
        await ctx.send(embed=embed)

    @commands.command(name="banner")
    async def view_banner(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]] = None):
        target = user or ctx.author
        fetched = await self.bot.fetch_user(target.id)
        if not fetched.banner:
            return await ctx.send("This user does not have a profile banner set.")
        url = fetched.banner.with_size(1024).url
        embed = discord.Embed(title=f"Banner for {target.display_name}", color=BOT_COLOR)
        embed.set_image(url=url)
        embed.add_field(name="Links", value=f"[Direct Link]({url})")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))

