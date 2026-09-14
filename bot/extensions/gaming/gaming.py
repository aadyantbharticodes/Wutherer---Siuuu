from __future__ import annotations
from typing import Optional
import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_mod
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR
from services.minecraft import MinecraftService
from database.models.minecraft import MinecraftServerModel


class Gaming(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.mc = MinecraftService()

    @commands.group(name="minecraft", aliases=["mc"], invoke_without_command=True)
    async def mc_group(self, ctx: commands.Context):
        await ctx.send_help(ctx.command)

    @mc_group.command(name="server", aliases=["status"])
    async def mc_server(self, ctx: commands.Context, address: str, server_type: str = "java"):
        async with ctx.typing():
            res = await self.mc.get_server_status(address, server_type=server_type)
            if not res or not res.get("online"):
                return await ctx.send(embed=discord.Embed(
                    title="🔴 Server Offline",
                    description=f"Could not connect to **{address}**.",
                    color=BOT_COLOR_ERROR
                ))

            motd = res.get("motd", {}).get("clean", "No MOTD provided")
            if isinstance(motd, list):
                motd = "\n".join(motd)

            embed = discord.Embed(
                title=f"🟢 {address} — Server Online",
                description=f"```\n{motd}\n```",
                color=BOT_COLOR_SUCCESS
            )
            embed.add_field(
                name="Players",
                value=f"{res.get('players', {}).get('online', 0):,} / {res.get('players', {}).get('max', 0):,}",
                inline=True
            )
            embed.add_field(
                name="Version",
                value=res.get("version", "Unknown"),
                inline=True
            )
            if res.get("icon"):
                embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{address}")
            await ctx.send(embed=embed)

    @mc_group.command(name="skin")
    async def mc_skin(self, ctx: commands.Context, username: str):
        uuid = await self.mc.get_uuid(username)
        if not uuid:
            return await ctx.send(f"Player **{username}** was not found.")

        skin_render_url = f"https://crafatar.com/renders/body/{uuid}?overlay=true"
        avatar_url = f"https://crafatar.com/avatars/{uuid}?overlay=true"

        embed = discord.Embed(
            title=f"Minecraft Skin — {username}",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_image(url=skin_render_url)
        embed.add_field(name="UUID", value=f"`{uuid}`", inline=False)
        await ctx.send(embed=embed)

    @mc_group.command(name="uuid")
    async def mc_uuid(self, ctx: commands.Context, username: str):
        uuid = await self.mc.get_uuid(username)
        if not uuid:
            return await ctx.send(f"Player **{username}** was not found.")
        embed = discord.Embed(
            title=f"Mojang Profile — {username}",
            description=f"**Username:** `{username}`\n**UUID:** `{uuid}`",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}?overlay=true")
        await ctx.send(embed=embed)

    @mc_group.command(name="track")
    @is_mod()
    async def mc_track(self, ctx: commands.Context, server_ip: str, channel: Optional[discord.TextChannel] = None):
        target_chan = channel or ctx.channel
        await MinecraftServerModel.add(
            self.bot.db, ctx.guild.id, target_chan.id, server_ip, setup_by=ctx.author.id
        )
        await ctx.send(embed=discord.Embed(
            description=f"Tracking status for **{server_ip}** in {target_chan.mention}.",
            color=BOT_COLOR_SUCCESS
        ))


async def setup(bot):
    await bot.add_cog(Gaming(bot))

