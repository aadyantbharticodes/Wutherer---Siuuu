from __future__ import annotations
import datetime
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_COLOR, BOT_COLOR_SUCCESS


class Social(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self._afk_cache: dict[tuple[int, int], str] = {}

    @commands.command(name="afk")
    async def set_afk(self, ctx: commands.Context, *, reason: str = "AFK"):
        await self.bot.db.execute(
            "INSERT INTO afk (guild_id, user_id, reason) VALUES (?, ?, ?) ON CONFLICT(guild_id, user_id) DO UPDATE SET reason=excluded.reason, set_at=datetime('now')",
            ctx.guild.id, ctx.author.id, reason
        )
        self._afk_cache[(ctx.guild.id, ctx.author.id)] = reason
        await ctx.send(embed=discord.Embed(
            description=f"💤 {ctx.author.mention}, I set your AFK: **{reason}**",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="profile")
    async def view_profile(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        target = member or ctx.author
        row = await self.bot.db.fetchrow("SELECT * FROM user_settings WHERE user_id = ?", target.id)
        badges = row.get("badges", "[]") if row else "[]"

        embed = discord.Embed(
            title=f"👤 {target.display_name}'s Profile",
            color=BOT_COLOR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Username", value=f"`{target}`", inline=True)
        embed.add_field(name="Account Created", value=f"<t:{int(target.created_at.timestamp())}:D>", inline=True)
        embed.add_field(name="Joined Server", value=f"<t:{int(target.joined_at.timestamp())}:D>" if target.joined_at else "Unknown", inline=True)
        embed.add_field(name="Top Role", value=target.top_role.mention, inline=True)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return


        afk_key = (message.guild.id, message.author.id)
        if afk_key in self._afk_cache or await self.bot.db.fetchrow(
            "SELECT 1 FROM afk WHERE guild_id = ? AND user_id = ?", message.guild.id, message.author.id
        ):
            self._afk_cache.pop(afk_key, None)
            await self.bot.db.execute(
                "DELETE FROM afk WHERE guild_id = ? AND user_id = ?", message.guild.id, message.author.id
            )
            try:
                msg = await message.channel.send(f"👋 Welcome back {message.author.mention}, I've removed your AFK.")
                await msg.delete(delay=5)
            except discord.HTTPException:
                pass


        for mentioned in message.mentions:
            if mentioned.bot:
                continue
            row = await self.bot.db.fetchrow(
                "SELECT reason, set_at FROM afk WHERE guild_id = ? AND user_id = ?",
                message.guild.id, mentioned.id
            )
            if row:
                embed = discord.Embed(
                    description=f"💤 **{mentioned.display_name}** is currently AFK: {row['reason']}",
                    color=BOT_COLOR
                )
                try:
                    await message.channel.send(embed=embed)
                except discord.HTTPException:
                    pass


async def setup(bot):
    await bot.add_cog(Social(bot))

