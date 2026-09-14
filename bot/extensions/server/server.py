from __future__ import annotations
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_admin, is_mod
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR
from database.models.guild import GuildSettings, WelcomeConfig, Autoroles, ReactionRoles


class Server(WuthererCog):

    @commands.command(name="setprefix", aliases=["prefix"])
    @is_admin()
    async def set_prefix(self, ctx: commands.Context, new_prefix: str):
        if len(new_prefix) > 10:
            return await ctx.send("Prefix cannot exceed 10 characters.")
        await GuildSettings.update(self.bot.db, ctx.guild.id, prefix=new_prefix)
        await ctx.send(embed=discord.Embed(
            description=f"Server prefix has been changed to `{new_prefix}`.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.group(name="welcome", invoke_without_command=True)
    @is_admin()
    async def welcome_group(self, ctx: commands.Context):
        cfg = await WelcomeConfig.get(self.bot.db, ctx.guild.id)
        chan = ctx.guild.get_channel(cfg.get("channel_id")) if cfg.get("channel_id") else None
        embed = discord.Embed(
            title="👋 Welcome Configuration",
            color=BOT_COLOR
        )
        embed.add_field(name="Status", value="Enabled" if cfg.get("enabled") else "Disabled", inline=True)
        embed.add_field(name="Channel", value=chan.mention if chan else "Not set", inline=True)
        embed.add_field(name="Message", value=f"```\n{cfg.get('message', 'Default')}\n```", inline=False)
        await ctx.send(embed=embed)

    @welcome_group.command(name="channel")
    @is_admin()
    async def set_welcome_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        await WelcomeConfig.update(self.bot.db, ctx.guild.id, enabled=1, channel_id=channel.id)
        await ctx.send(embed=discord.Embed(
            description=f"Welcome messages will now be posted to {channel.mention}.",
            color=BOT_COLOR_SUCCESS
        ))

    @welcome_group.command(name="message")
    @is_admin()
    async def set_welcome_message(self, ctx: commands.Context, *, message: str):
        await WelcomeConfig.update(self.bot.db, ctx.guild.id, message=message)
        await ctx.send(embed=discord.Embed(
            description="Welcome message updated!",
            color=BOT_COLOR_SUCCESS
        ))

    @welcome_group.command(name="testcard", aliases=["cardpreview"])
    @is_admin()
    async def test_welcome_card(self, ctx: commands.Context):
        from bot.services.welcome_card import WelcomeCardGenerator
        avatar_bytes = None
        try:
            avatar_bytes = await ctx.author.display_avatar.read()
        except Exception:
            pass

        card_buf = WelcomeCardGenerator.create_card(
            member_name=ctx.author.name,
            guild_name=ctx.guild.name,
            member_count=ctx.guild.member_count,
            avatar_bytes=avatar_bytes,
        )
        file = discord.File(card_buf, filename=f"welcome_{ctx.author.id}.png")
        await ctx.send("🎨 Generated Sentinel Dynamic Welcome Banner:", file=file)


    @commands.group(name="autorole", invoke_without_command=True)
    @is_admin()
    async def autorole_group(self, ctx: commands.Context):
        roles_data = await Autoroles.get(self.bot.db, ctx.guild.id)
        if not roles_data:
            return await ctx.send("No autoroles currently configured.")
        lines = []
        for r_entry in roles_data:
            role = ctx.guild.get_role(r_entry["role_id"])
            if role:
                lines.append(f"• {role.mention} (Target: `{r_entry['target']}`)")
        embed = discord.Embed(
            title="🛡️ Autoroles",
            description="\n".join(lines),
            color=BOT_COLOR
        )
        await ctx.send(embed=embed)

    @autorole_group.command(name="add")
    @is_admin()
    async def add_autorole(self, ctx: commands.Context, role: discord.Role, target: str = "all"):
        if target.lower() not in ("all", "human", "bot"):
            return await ctx.send("Target must be `all`, `human`, or `bot`.")
        if role >= ctx.guild.me.top_role:
            return await ctx.send("I cannot assign a role higher than or equal to my own top role.")

        await Autoroles.add(self.bot.db, ctx.guild.id, role.id, target.lower())
        await ctx.send(embed=discord.Embed(
            description=f"Added {role.mention} as an autorole for `{target.lower()}`.",
            color=BOT_COLOR_SUCCESS
        ))

    @autorole_group.command(name="remove")
    @is_admin()
    async def remove_autorole(self, ctx: commands.Context, role: discord.Role):
        await Autoroles.remove(self.bot.db, ctx.guild.id, role.id)
        await ctx.send(embed=discord.Embed(
            description=f"Removed {role.mention} from autoroles.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="reactionrole", aliases=["rr"])
    @is_admin()
    async def setup_reaction_role(
        self, ctx: commands.Context, message_id: int, emoji: str, role: discord.Role
    ):
        if role >= ctx.guild.me.top_role:
            return await ctx.send("That role is too high for me to assign.")
        try:
            target_msg = await ctx.channel.fetch_message(message_id)
            await target_msg.add_reaction(emoji)
        except (discord.NotFound, discord.HTTPException):
            return await ctx.send("Could not find that message or add the reaction.")

        await ReactionRoles.add(self.bot.db, ctx.guild.id, ctx.channel.id, message_id, emoji, role.id)
        await ctx.send(embed=discord.Embed(
            description=f"Reaction role created! Reacting with {emoji} on message `{message_id}` will grant {role.mention}.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if not payload.guild_id or payload.user_id == self.bot.user.id:
            return
        emoji_str = str(payload.emoji)
        rr = await ReactionRoles.get(self.bot.db, payload.message_id, emoji_str)
        if not rr:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        member = guild.get_member(payload.user_id)
        role = guild.get_role(rr["role_id"])
        if member and role and guild.me.guild_permissions.manage_roles and role < guild.me.top_role:
            try:
                await member.add_roles(role, reason="Sentinel Reaction Role")
            except discord.HTTPException:
                pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if not payload.guild_id or payload.user_id == self.bot.user.id:
            return
        emoji_str = str(payload.emoji)
        rr = await ReactionRoles.get(self.bot.db, payload.message_id, emoji_str)
        if not rr:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        member = guild.get_member(payload.user_id)
        role = guild.get_role(rr["role_id"])
        if member and role and guild.me.guild_permissions.manage_roles and role < guild.me.top_role:
            try:
                await member.remove_roles(role, reason="Sentinel Reaction Role Removed")
            except discord.HTTPException:
                pass


async def setup(bot):
    await bot.add_cog(Server(bot))

