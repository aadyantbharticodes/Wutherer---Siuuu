from __future__ import annotations
import asyncio
import logging
from typing import Optional, Union
import discord
from discord.ext import commands

from database.models.antinuke import AntiNukeModel
from services.antinuke import AntiNukeService

log = logging.getLogger("sentinel.nuke_cog")


class NukeDefenseCog(commands.Cog, name="Server Defense"):
    def __init__(self, bot):
        self.bot = bot
        self.service = AntiNukeService(bot, bot.db)

    @commands.command(name="nuke", description="Purge and recreate the current channel with identical permissions and topic")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def nuke_channel(self, ctx: commands.Context):
        channel = ctx.channel
        if not isinstance(channel, discord.TextChannel):
            await ctx.send("❌ This command can only be run in text channels.")
            return

        pos = channel.position
        cat = channel.category
        topic = channel.topic
        slow = channel.slowmode_delay
        ow = channel.overwrites
        name = channel.name

        msg = await ctx.send("⚠️ **Channel nuke initiated!** Cloning channel and purging legacy messages...")
        await asyncio.sleep(1.0)

        new_channel = await ctx.guild.create_text_channel(
            name=name,
            category=cat,
            topic=topic,
            slowmode_delay=slow,
            overwrites=ow,
            position=pos,
            reason=f"Channel nuked by {ctx.author}"
        )

        try:
            await channel.delete(reason=f"Channel nuked by {ctx.author}")
        except Exception as e:
            await new_channel.send(f"⚠️ Failed deleting old channel: {e}")

        embed = discord.Embed(
            title="💣 Channel Nuked",
            description=f"This channel was completely purged and recreated by {ctx.author.mention}.",
            color=0xED4245
        )
        embed.set_image(url="https://media.giphy.com/media/oe33xf3B50fsc/giphy.gif")
        embed.set_footer(text="Sentinel Defense Suite")
        await new_channel.send(embed=embed)

    @commands.command(name="clone", description="Clone a channel with identical configuration")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def clone_channel(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        target = channel or ctx.channel
        if not isinstance(target, discord.TextChannel):
            await ctx.send("❌ Target must be a text channel.")
            return

        cloned = await target.clone(reason=f"Channel cloned by {ctx.author}")
        await ctx.send(f"✅ Cloned channel {target.mention} -> {cloned.mention}")

    @commands.command(name="lockdown", aliases=["panic", "lock"], description="Lock down the current channel or the entire server")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lockdown(self, ctx: commands.Context, target: Optional[str] = None):
        if target and target.lower() in ("all", "server", "guild"):
            status_msg = await ctx.send("🚨 **Initiating Emergency Panic Lockdown across the entire server...**")
            res = await self.service.panic_lockdown(ctx.guild)
            embed = discord.Embed(
                title="🔒 Emergency Panic Lockdown Active",
                description=f"Sentinel locked **{res['channels_locked']}** channels to protect the server from active raids.",
                color=0xED4245
            )
            embed.set_footer(text="Run 's!unlock all' to lift lockdown")
            await status_msg.edit(content=None, embed=embed)
        else:
            channel = ctx.channel
            everyone = ctx.guild.default_role
            ow = channel.overwrites_for(everyone)
            ow.send_messages = False
            ow.send_messages_in_threads = False
            await channel.set_permissions(everyone, overwrite=ow, reason=f"Lockdown by {ctx.author}")
            embed = discord.Embed(
                title="🔒 Channel Locked",
                description=f"{channel.mention} has been locked down by {ctx.author.mention}.",
                color=0xED4245
            )
            await ctx.send(embed=embed)

    @commands.command(name="unlock", description="Unlock a channel or lift server-wide panic lockdown")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx: commands.Context, target: Optional[str] = None):
        if target and target.lower() in ("all", "server", "guild"):
            status_msg = await ctx.send("🔓 **Restoring channel permissions and lifting lockdown...**")
            res = await self.service.lift_lockdown(ctx.guild)
            embed = discord.Embed(
                title="🔓 Panic Lockdown Lifted",
                description=f"Restored permissions for **{res['channels_unlocked']}** channels.",
                color=0x57F287
            )
            await status_msg.edit(content=None, embed=embed)
        else:
            channel = ctx.channel
            everyone = ctx.guild.default_role
            ow = channel.overwrites_for(everyone)
            ow.send_messages = None
            ow.send_messages_in_threads = None
            await channel.set_permissions(everyone, overwrite=ow, reason=f"Unlocked by {ctx.author}")
            embed = discord.Embed(
                title="🔓 Channel Unlocked",
                description=f"{channel.mention} is now unlocked.",
                color=0x57F287
            )
            await ctx.send(embed=embed)

    @commands.command(name="raidmode", description="Toggle anti-raid emergency gate")
    @commands.has_permissions(administrator=True)
    async def raidmode(self, ctx: commands.Context, state: str = "on"):
        enable = state.lower() in ("on", "enable", "true", "1")
        if enable:
            await ctx.guild.edit(
                verification_level=discord.VerificationLevel.high,
                reason=f"Sentinel Raid Mode enabled by {ctx.author}"
            )
            embed = discord.Embed(
                title="🛡️ Raid Mode Enabled",
                description="Server verification level elevated to **HIGH**. All incoming raids will be strictly throttled.",
                color=0xED4245
            )
        else:
            await ctx.guild.edit(
                verification_level=discord.VerificationLevel.medium,
                reason=f"Sentinel Raid Mode disabled by {ctx.author}"
            )
            embed = discord.Embed(
                title="🛡️ Raid Mode Disabled",
                description="Server verification returned to standard **MEDIUM** level.",
                color=0x57F287
            )
        await ctx.send(embed=embed)

    @commands.command(name="quarantine", description="Isolate a suspicious member into a quarantine role")
    @commands.has_permissions(manage_roles=True)
    async def quarantine_member(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Suspected compromised account"):
        cfg = await AntiNukeModel.get_config(self.bot.db, ctx.guild.id)
        q_role_id = cfg.get("quarantine_role_id")
        q_role = ctx.guild.get_role(q_role_id) if q_role_id else None

        if not q_role:
            q_role = discord.utils.get(ctx.guild.roles, name="Quarantined")
            if not q_role:
                try:
                    q_role = await ctx.guild.create_role(
                        name="Quarantined",
                        color=discord.Color.dark_grey(),
                        reason="Sentinel Quarantine Role"
                    )
                    for ch in ctx.guild.channels:
                        await ch.set_permissions(q_role, send_messages=False, connect=False, read_messages=False)
                    await AntiNukeModel.update_config(self.bot.db, ctx.guild.id, quarantine_role_id=q_role.id)
                except Exception as e:
                    await ctx.send(f"❌ Could not create quarantine role: {e}")
                    return

        roles_to_remove = [r for r in member.roles if not r.is_default() and not r.managed]
        await member.remove_roles(*roles_to_remove, reason=f"Quarantine by {ctx.author}: {reason}")
        await member.add_roles(q_role, reason=f"Quarantine by {ctx.author}: {reason}")

        embed = discord.Embed(
            title="☣️ Member Quarantined",
            description=f"{member.mention} has been isolated from all server channels.\n**Reason:** {reason}",
            color=0x95A5A6
        )
        await ctx.send(embed=embed)

    @commands.group(name="antinuke", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def antinuke_group(self, ctx: commands.Context):
        cfg = await AntiNukeModel.get_config(self.bot.db, ctx.guild.id)
        embed = discord.Embed(
            title="🛡️ Wutherer Anti-Nuke Shield Status",
            color=0x57F287 if cfg.get("enabled") else 0xED4245
        )
        embed.description = f"Status: **{'ACTIVE' if cfg.get('enabled') else 'DISABLED'}**\nAction Type: **{cfg.get('action_type', 'ban').upper()}**\nWindow: **{cfg.get('rate_window_seconds', 15)}s**"
        embed.add_field(name="Channel Delete Limit", value=f"**{cfg.get('max_channel_deletes', 3)}** actions", inline=True)
        embed.add_field(name="Role Delete Limit", value=f"**{cfg.get('max_role_deletes', 3)}** actions", inline=True)
        embed.add_field(name="Mass Ban Limit", value=f"**{cfg.get('max_bans', 5)}** actions", inline=True)
        embed.add_field(name="Webhook Create Limit", value=f"**{cfg.get('max_webhook_creates', 2)}** actions", inline=True)
        embed.add_field(name="Commands", value=(
            "`s!antinuke toggle` — Enable/disable anti-nuke shield\n"
            "`s!antinuke whitelist add/remove <@user>` — Trust admins\n"
            "`s!antinuke logs` — View recent security audit records"
        ), inline=False)
        await ctx.send(embed=embed)

    @antinuke_group.command(name="toggle")
    @commands.has_permissions(administrator=True)
    async def antinuke_toggle(self, ctx: commands.Context):
        cfg = await AntiNukeModel.get_config(self.bot.db, ctx.guild.id)
        new_state = 0 if cfg.get("enabled") else 1
        await AntiNukeModel.update_config(self.bot.db, ctx.guild.id, enabled=new_state)
        await ctx.send(f"🛡️ Anti-Nuke Shield is now **{'ENABLED' if new_state else 'DISABLED'}**.")

    @antinuke_group.command(name="whitelist")
    @commands.has_permissions(administrator=True)
    async def antinuke_whitelist(self, ctx: commands.Context, action: str, member: discord.Member):
        if action.lower() == "add":
            await AntiNukeModel.add_whitelist(self.bot.db, ctx.guild.id, member.id, "user")
            await ctx.send(f"✅ Added {member.mention} to Anti-Nuke Whitelist.")
        elif action.lower() in ("remove", "delete"):
            await AntiNukeModel.remove_whitelist(self.bot.db, ctx.guild.id, member.id)
            await ctx.send(f"🗑️ Removed {member.mention} from Anti-Nuke Whitelist.")
        else:
            await ctx.send("❌ Usage: `s!antinuke whitelist <add/remove> <@user>`")

    @antinuke_group.command(name="logs")
    @commands.has_permissions(administrator=True)
    async def antinuke_logs(self, ctx: commands.Context):
        logs = await AntiNukeModel.get_logs(self.bot.db, ctx.guild.id, limit=8)
        if not logs:
            await ctx.send("ℹ️ No anti-nuke violations recorded recently.")
            return

        embed = discord.Embed(title="🚨 Anti-Nuke Security Audit Logs", color=0xED4245)
        for entry in logs:
            embed.add_field(
                name=f"⚠️ {entry['event_type']} — <@{entry['culprit_id']}>",
                value=f"Action: **{entry.get('action_taken')}**\n{entry.get('details')}\n`{entry.get('created_at')}`",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        guild = channel.guild
        cfg = await AntiNukeModel.get_config(self.bot.db, guild.id)
        if not cfg.get("enabled"):
            return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            if entry.user:
                await self.service.check_violation(
                    guild,
                    entry.user.id,
                    "channel_delete",
                    cfg.get("max_channel_deletes", 3)
                )
            break

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        guild = role.guild
        cfg = await AntiNukeModel.get_config(self.bot.db, guild.id)
        if not cfg.get("enabled"):
            return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            if entry.user:
                await self.service.check_violation(
                    guild,
                    entry.user.id,
                    "role_delete",
                    cfg.get("max_role_deletes", 3)
                )
            break

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: Union[discord.User, discord.Member]):
        cfg = await AntiNukeModel.get_config(self.bot.db, guild.id)
        if not cfg.get("enabled"):
            return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.user:
                await self.service.check_violation(
                    guild,
                    entry.user.id,
                    "member_ban",
                    cfg.get("max_bans", 5)
                )
            break


async def setup(bot):
    await bot.add_cog(NukeDefenseCog(bot))
