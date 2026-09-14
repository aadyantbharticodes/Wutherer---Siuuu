from __future__ import annotations
import json
from typing import Optional
import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_admin, is_mod
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR
from database.models.automation import CustomCommands, StickyMessages


class Automation(WuthererCog):

    @commands.group(name="customcommand", aliases=["cc", "tag"], invoke_without_command=True)
    async def cc_group(self, ctx: commands.Context, *, name: Optional[str] = None):
        if not name:
            return await ctx.send_help(ctx.command)
        cmd = await CustomCommands.get(self.bot.db, ctx.guild.id, name)
        if not cmd:
            return await ctx.send(f"Custom command `{name}` does not exist.")
        await CustomCommands.increment_uses(self.bot.db, cmd["id"])
        await ctx.send(cmd["response"])

    @cc_group.command(name="add", aliases=["create"])
    @is_mod()
    async def cc_add(self, ctx: commands.Context, name: str, *, response: str):
        name = name.lower()
        if self.bot.get_command(name):
            return await ctx.send(f"Cannot overwrite built-in command `{name}`.")
        await CustomCommands.add(self.bot.db, ctx.guild.id, name, response, ctx.author.id)
        await ctx.send(embed=discord.Embed(
            description=f"Successfully saved custom command `{name}`.",
            color=BOT_COLOR_SUCCESS
        ))

    @cc_group.command(name="delete", aliases=["del", "remove"])
    @is_mod()
    async def cc_delete(self, ctx: commands.Context, name: str):
        deleted = await CustomCommands.delete(self.bot.db, ctx.guild.id, name)
        if deleted:
            await ctx.send(embed=discord.Embed(
                description=f"Deleted custom command `{name}`.",
                color=BOT_COLOR_SUCCESS
            ))
        else:
            await ctx.send(f"Custom command `{name}` was not found.")

    @cc_group.command(name="list")
    async def cc_list(self, ctx: commands.Context):
        cmds = await CustomCommands.get_all(self.bot.db, ctx.guild.id)
        if not cmds:
            return await ctx.send("No custom commands configured in this server.")
        names = [f"`{c['name']}` ({c['uses']} uses)" for c in cmds]
        embed = discord.Embed(
            title=f"Custom Commands ({len(cmds)})",
            description=", ".join(names),
            color=BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.group(name="sticky", invoke_without_command=True)
    @is_admin()
    async def sticky_group(self, ctx: commands.Context):
        await ctx.send_help(ctx.command)

    @sticky_group.command(name="set")
    @is_admin()
    async def sticky_set(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None, *, message: str):
        target_channel = channel or ctx.channel
        await StickyMessages.set(self.bot.db, ctx.guild.id, target_channel.id, message)
        await ctx.send(embed=discord.Embed(
            description=f"Sticky message configured in {target_channel.mention}.",
            color=BOT_COLOR_SUCCESS
        ))

    @sticky_group.command(name="remove", aliases=["clear"])
    @is_admin()
    async def sticky_remove(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        target_channel = channel or ctx.channel
        await StickyMessages.remove(self.bot.db, target_channel.id)
        await ctx.send(embed=discord.Embed(
            description=f"Removed sticky message from {target_channel.mention}.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return


        sticky = await StickyMessages.get(self.bot.db, message.channel.id)
        if sticky:
            try:
                old_id = sticky.get("message_id")
                if old_id:
                    try:
                        old_msg = await message.channel.fetch_message(old_id)
                        await old_msg.delete()
                    except discord.NotFound:
                        pass
                new_msg = await message.channel.send(f"📌 **Sticky Notice:**\n{sticky['content']}")
                await StickyMessages.update_message(self.bot.db, message.channel.id, new_msg.id)
            except discord.HTTPException:
                pass


async def setup(bot):
    await bot.add_cog(Automation(bot))

