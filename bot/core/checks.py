from __future__ import annotations
import discord
from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.context import Context


def is_server_owner():
    async def predicate(ctx: Context) -> bool:
        if ctx.author.id == ctx.guild.owner_id:
            return True
        raise commands.CheckFailure("Only the server owner can use this command.")
    return commands.check(predicate)


def is_admin():
    async def predicate(ctx: Context) -> bool:
        if ctx.author.guild_permissions.administrator:
            return True
        raise commands.CheckFailure("You need Administrator permission.")
    return commands.check(predicate)


def is_mod():
    async def predicate(ctx: Context) -> bool:
        perms = ctx.author.guild_permissions
        if perms.administrator or perms.manage_guild or perms.ban_members or perms.kick_members:
            return True
        raise commands.CheckFailure("You need moderation permissions.")
    return commands.check(predicate)


def can_moderate(target: discord.Member, moderator: discord.Member, guild: discord.Guild) -> bool:
    if target.id == guild.owner_id:
        return False
    if moderator.id == guild.owner_id:
        return True
    if target.top_role >= moderator.top_role:
        return False
    bot_member = guild.me
    if target.top_role >= bot_member.top_role:
        return False
    return True


def has_guild_permissions(**perms):
    async def predicate(ctx: Context) -> bool:
        resolved = ctx.author.guild_permissions
        missing = [p for p, v in perms.items() if getattr(resolved, p, None) != v]
        if not missing:
            return True
        raise commands.MissingPermissions(missing)
    return commands.check(predicate)


def bot_has_permissions(**perms):
    async def predicate(ctx: Context) -> bool:
        bot_perms = ctx.guild.me.guild_permissions
        missing = [p for p, v in perms.items() if getattr(bot_perms, p, None) != v]
        if not missing:
            return True
        raise commands.BotMissingPermissions(missing)
    return commands.check(predicate)

