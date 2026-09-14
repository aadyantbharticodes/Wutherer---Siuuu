from __future__ import annotations
from typing import Optional, Union
import discord
from discord.ext import commands


class PermissionManager:

    @staticmethod
    def is_guild_owner(member: discord.Member) -> bool:
        return member.id == member.guild.owner_id

    @staticmethod
    def is_administrator(member: discord.Member) -> bool:
        return member.guild_permissions.administrator or PermissionManager.is_guild_owner(member)

    @staticmethod
    def can_moderate_member(moderator: discord.Member, target: discord.Member) -> bool:
        if target.id == moderator.guild.owner_id:
            return False
        if moderator.id == moderator.guild.owner_id:
            return True
        if target.top_role >= moderator.top_role:
            return False
        bot_member = moderator.guild.me
        if target.top_role >= bot_member.top_role:
            return False
        return True

    @staticmethod
    def has_permissions(member: discord.Member, channel: Optional[discord.abc.GuildChannel] = None, **perms) -> bool:
        if channel:
            resolved = channel.permissions_for(member)
        else:
            resolved = member.guild_permissions

        if resolved.administrator:
            return True

        for perm, value in perms.items():
            if getattr(resolved, perm, None) != value:
                return False
        return True

    @staticmethod
    def missing_permissions(member: discord.Member, channel: Optional[discord.abc.GuildChannel] = None, **perms) -> list[str]:
        if channel:
            resolved = channel.permissions_for(member)
        else:
            resolved = member.guild_permissions

        if resolved.administrator:
            return []

        missing = []
        for perm, value in perms.items():
            if getattr(resolved, perm, None) != value:
                missing.append(perm.replace("_", " ").title())
        return missing

