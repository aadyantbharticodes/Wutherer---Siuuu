from __future__ import annotations
import io
import sys
import textwrap
import traceback
import time
from contextlib import redirect_stdout
from typing import Optional, Literal

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_NAME, BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR


class Admin(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self._last_result = None

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="reload", aliases=["rl"])
    async def reload_extension(self, ctx: commands.Context, *, extension: str):
        ext_target = extension if extension.startswith("extensions.") else f"extensions.{extension}"
        try:
            await self.bot.reload_extension(ext_target)
            await ctx.send(embed=discord.Embed(
                description=f"Successfully reloaded `{ext_target}`.",
                color=BOT_COLOR_SUCCESS
            ))
        except Exception as exc:
            await ctx.send(embed=discord.Embed(
                description=f"Failed to reload `{ext_target}`:\n```py\n{exc}\n```",
                color=BOT_COLOR_ERROR
            ))

    @commands.command(name="load")
    async def load_extension(self, ctx: commands.Context, *, extension: str):
        ext_target = extension if extension.startswith("extensions.") else f"extensions.{extension}"
        try:
            await self.bot.load_extension(ext_target)
            await ctx.send(embed=discord.Embed(
                description=f"Successfully loaded `{ext_target}`.",
                color=BOT_COLOR_SUCCESS
            ))
        except Exception as exc:
            await ctx.send(embed=discord.Embed(
                description=f"Failed to load `{ext_target}`:\n```py\n{exc}\n```",
                color=BOT_COLOR_ERROR
            ))

    @commands.command(name="unload")
    async def unload_extension(self, ctx: commands.Context, *, extension: str):
        ext_target = extension if extension.startswith("extensions.") else f"extensions.{extension}"
        try:
            await self.bot.unload_extension(ext_target)
            await ctx.send(embed=discord.Embed(
                description=f"Successfully unloaded `{ext_target}`.",
                color=BOT_COLOR_SUCCESS
            ))
        except Exception as exc:
            await ctx.send(embed=discord.Embed(
                description=f"Failed to unload `{ext_target}`:\n```py\n{exc}\n```",
                color=BOT_COLOR_ERROR
            ))

    @commands.command(name="sync")
    async def sync_app_commands(self, ctx: commands.Context, spec: Optional[Literal["guild", "global", "clear"]] = "global"):
        if spec == "guild":
            synced = await self.bot.tree.sync(guild=ctx.guild)
            await ctx.send(f"Synced {len(synced)} slash commands to current guild.")
        elif spec == "clear":
            self.bot.tree.clear_commands(guild=ctx.guild)
            await self.bot.tree.sync(guild=ctx.guild)
            await ctx.send("Cleared slash commands in this guild.")
        else:
            synced = await self.bot.tree.sync()
            await ctx.send(f"Globally synced {len(synced)} slash commands.")

    @commands.command(name="eval", aliases=["ev"])
    async def eval_code(self, ctx: commands.Context, *, code: str):
        code = code.strip("` ")
        if code.startswith("py\n"):
            code = code[3:]

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
            "db": self.bot.db
        }
        env.update(globals())

        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as exc:
            return await ctx.send(f"```py\n{exc.__class__.__name__}: {exc}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            val = stdout.getvalue()
            return await ctx.send(f"```py\n{val}{traceback.format_exc()}\n```")

        value = stdout.getvalue()
        if ret is None:
            if value:
                await ctx.send(f"```py\n{value}\n```")
        else:
            self._last_result = ret
            await ctx.send(f"```py\n{value}{ret}\n```")

    @commands.command(name="leaveguild")
    async def leave_guild(self, ctx: commands.Context, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.send("Guild not found.")
        await guild.leave()
        await ctx.send(f"Left guild: **{guild.name}** (`{guild.id}`).")

    @commands.command(name="blacklist")
    async def blacklist_user(self, ctx: commands.Context, user: discord.User, *, reason: str = "Violating bot terms"):
        from database.models.user import Blacklist
        await Blacklist.add(self.bot.db, user.id, reason, ctx.author.id)
        await ctx.send(f"Blacklisted **{user}** (`{user.id}`). Reason: {reason}")

    @commands.command(name="unblacklist")
    async def unblacklist_user(self, ctx: commands.Context, user: discord.User):
        from database.models.user import Blacklist
        await Blacklist.remove(self.bot.db, user.id)
        await ctx.send(f"Unblacklisted **{user}** (`{user.id}`).")

    @commands.command(name="broadcast")
    async def broadcast_announcement(self, ctx: commands.Context, *, message: str):
        sent = 0
        embed = discord.Embed(
            title=f"📢 {BOT_NAME} Announcement",
            description=message,
            color=BOT_COLOR,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Official Sentinel Broadcast")

        for guild in self.bot.guilds:
            channel = guild.system_channel
            if not channel:
                channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
            if channel:
                try:
                    await channel.send(embed=embed)
                    sent += 1
                except discord.HTTPException:
                    pass
        await ctx.send(f"Broadcast delivered to {sent}/{len(self.bot.guilds)} servers.")


async def setup(bot):
    await bot.add_cog(Admin(bot))

