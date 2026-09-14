from __future__ import annotations
import asyncio
import discord
from discord.ext import commands
from typing import Optional

from database.models.onboarding import AdvancedWelcomeModel
from services.onboarding_service import OnboardingService


class WelcomeAdvancedCog(commands.Cog, name="Onboarding"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="farewell", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def farewell_group(self, ctx: commands.Context):
        cfg = await AdvancedWelcomeModel.get(self.bot.db, ctx.guild.id)
        embed = discord.Embed(
            title="👋 Farewell & Departure Announcements",
            color=0x57F287 if cfg.get("farewell_enabled") else 0xED4245
        )
        embed.description = f"Status: **{'ENABLED' if cfg.get('farewell_enabled') else 'DISABLED'}**"
        ch_id = cfg.get("farewell_channel_id")
        embed.add_field(name="Announcement Channel", value=f"<#{ch_id}>" if ch_id else "*Not configured*", inline=True)
        embed.add_field(name="Current Message", value=f"```\n{cfg.get('farewell_message', 'Goodbye {user.name}!')}\n```", inline=False)
        embed.add_field(name="Commands", value=(
            "`s!farewell toggle` — Enable/disable farewell announcements\n"
            "`s!farewell channel <#channel>` — Set broadcast channel\n"
            "`s!farewell message <text>` — Set custom goodbye message\n"
            "`s!farewell test` — Test farewell broadcast"
        ), inline=False)
        embed.set_footer(text="Variables: {user}, {user.name}, {guild.name}, {guild.member_count}")
        await ctx.send(embed=embed)

    @farewell_group.command(name="toggle")
    @commands.has_permissions(manage_guild=True)
    async def farewell_toggle(self, ctx: commands.Context):
        cfg = await AdvancedWelcomeModel.get(self.bot.db, ctx.guild.id)
        new_state = 0 if cfg.get("farewell_enabled") else 1
        await AdvancedWelcomeModel.update(self.bot.db, ctx.guild.id, farewell_enabled=new_state)
        await ctx.send(f"👋 Farewell announcements are now **{'ENABLED' if new_state else 'DISABLED'}**.")

    @farewell_group.command(name="channel")
    @commands.has_permissions(manage_guild=True)
    async def farewell_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        await AdvancedWelcomeModel.update(self.bot.db, ctx.guild.id, farewell_channel_id=channel.id)
        await ctx.send(f"✅ Farewell announcements channel set to {channel.mention}.")

    @farewell_group.command(name="message")
    @commands.has_permissions(manage_guild=True)
    async def farewell_message(self, ctx: commands.Context, *, text: str):
        await AdvancedWelcomeModel.update(self.bot.db, ctx.guild.id, farewell_message=text)
        await ctx.send("✅ Farewell announcement message updated!")

    @farewell_group.command(name="test")
    @commands.has_permissions(manage_guild=True)
    async def farewell_test(self, ctx: commands.Context):
        cfg = await AdvancedWelcomeModel.get(self.bot.db, ctx.guild.id)
        ch_id = cfg.get("farewell_channel_id")
        channel = ctx.guild.get_channel(ch_id) if ch_id else ctx.channel
        if not isinstance(channel, discord.TextChannel):
            await ctx.send("❌ Valid text channel not configured.")
            return

        text = OnboardingService.interpolate(cfg.get("farewell_message", "Goodbye {user.name}!"), ctx.author)
        embed = discord.Embed(
            title="👋 Member Departed",
            description=text,
            color=0xED4245
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        await channel.send(embed=embed)
        await ctx.send(f"✅ Dispatched test farewell in {channel.mention}.")

    @commands.group(name="delayedrole", invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def delayed_role_group(self, ctx: commands.Context):
        cfg = await AdvancedWelcomeModel.get(self.bot.db, ctx.guild.id)
        mins = cfg.get("autorole_delay_minutes", 0)
        roles = cfg.get("autorole_delay_roles", [])
        role_mentions = [f"<@&{rid}>" for rid in roles] if roles else ["*None*"]

        embed = discord.Embed(
            title="⏱️ Timed / Delayed Autoroles",
            description="Assign specific roles after a member has been in the server for a specified duration.",
            color=0x5865F2
        )
        embed.add_field(name="Delay Duration", value=f"**{mins}** minute(s)", inline=True)
        embed.add_field(name="Roles to Assign", value=", ".join(role_mentions), inline=False)
        embed.add_field(name="Commands", value=(
            "`s!delayedrole delay <minutes>` — Set delay period\n"
            "`s!delayedrole add <@role>` — Add role to delayed assignment list\n"
            "`s!delayedrole remove <@role>` — Remove role from list\n"
            "`s!delayedrole clear` — Remove all delayed autoroles"
        ), inline=False)
        await ctx.send(embed=embed)

    @delayed_role_group.command(name="delay")
    @commands.has_permissions(manage_roles=True)
    async def delayed_role_delay(self, ctx: commands.Context, minutes: int):
        m = max(0, min(minutes, 1440))
        await AdvancedWelcomeModel.update(self.bot.db, ctx.guild.id, autorole_delay_minutes=m)
        await ctx.send(f"⏱️ Delayed autorole timer set to **{m}** minute(s).")

    @delayed_role_group.command(name="add")
    @commands.has_permissions(manage_roles=True)
    async def delayed_role_add(self, ctx: commands.Context, role: discord.Role):
        cfg = await AdvancedWelcomeModel.get(self.bot.db, ctx.guild.id)
        roles = cfg.get("autorole_delay_roles", [])
        if role.id in roles:
            await ctx.send(f"ℹ️ {role.mention} is already in the delayed autorole list.")
            return
        roles.append(role.id)
        await AdvancedWelcomeModel.update(self.bot.db, ctx.guild.id, autorole_delay_roles=roles)
        await ctx.send(f"✅ Added {role.mention} to delayed autoroles.")

    @delayed_role_group.command(name="remove")
    @commands.has_permissions(manage_roles=True)
    async def delayed_role_remove(self, ctx: commands.Context, role: discord.Role):
        cfg = await AdvancedWelcomeModel.get(self.bot.db, ctx.guild.id)
        roles = cfg.get("autorole_delay_roles", [])
        if role.id not in roles:
            await ctx.send(f"ℹ️ {role.mention} is not in the list.")
            return
        roles.remove(role.id)
        await AdvancedWelcomeModel.update(self.bot.db, ctx.guild.id, autorole_delay_roles=roles)
        await ctx.send(f"🗑️ Removed {role.mention} from delayed autoroles.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        cfg = await AdvancedWelcomeModel.get(self.bot.db, member.guild.id)
        delay_mins = cfg.get("autorole_delay_minutes", 0)
        roles = cfg.get("autorole_delay_roles", [])

        if delay_mins > 0 and roles:
            asyncio.create_task(self._apply_delayed_roles(member, delay_mins, roles))

    async def _apply_delayed_roles(self, member: discord.Member, delay_mins: int, role_ids: list[int]):
        await asyncio.sleep(delay_mins * 60)
        guild = member.guild
        current_member = guild.get_member(member.id)
        if not current_member:
            return

        roles_to_add = []
        for rid in role_ids:
            r = guild.get_role(rid)
            if r and r not in current_member.roles:
                roles_to_add.append(r)

        if roles_to_add:
            try:
                await current_member.add_roles(*roles_to_add, reason="Wutherer Delayed Autorole Engine")
            except Exception:
                pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        cfg = await AdvancedWelcomeModel.get(self.bot.db, member.guild.id)
        if not cfg.get("farewell_enabled"):
            return

        ch_id = cfg.get("farewell_channel_id")
        channel = member.guild.get_channel(ch_id) if ch_id else None
        if not isinstance(channel, discord.TextChannel):
            return

        msg_template = cfg.get("farewell_message", "Goodbye {user.name}, we hope to see you again!")
        desc = OnboardingService.interpolate(msg_template, member)

        embed = discord.Embed(
            title="👋 Member Left",
            description=desc,
            color=0xED4245
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Total Members: {member.guild.member_count}")
        try:
            await channel.send(embed=embed)
        except Exception:
            pass


async def setup(bot):
    await bot.add_cog(WelcomeAdvancedCog(bot))
