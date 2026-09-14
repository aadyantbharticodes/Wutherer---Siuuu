from __future__ import annotations
import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR, BOT_COLOR_WARNING
from database.models.moderation import AntinukeConfig


class Antinuke(WuthererCog):

    @commands.group(name="antinuke", aliases=["an"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def antinuke(self, ctx):
        config = await AntinukeConfig.get(self.db, ctx.guild.id)
        embed = discord.Embed(color=BOT_COLOR, title="Antinuke Configuration")
        embed.add_field(name="Status", value="Enabled" if config.get("enabled") else "Disabled", inline=True)
        embed.add_field(name="Punishment", value=config.get("punishment", "ban").capitalize(), inline=True)
        modules = {
            "Anti-Bot": "antibot", "Anti-Ban": "antiban", "Anti-Kick": "antikick",
            "Anti-Channel Create": "antichannel_create", "Anti-Channel Delete": "antichannel_delete",
            "Anti-Channel Update": "antichannel_update", "Anti-Role Create": "antirole_create",
            "Anti-Role Delete": "antirole_delete", "Anti-Role Update": "antirole_update",
            "Anti-Webhook": "antiwebhook", "Anti-Guild Update": "antiguild_update",
            "Anti-Everyone": "antieveryone", "Anti-Prune": "antiprune",
            "Anti-Integration": "antiintegration",
        }
        for label, key in modules.items():
            status = "On" if config.get(key) else "Off"
            embed.add_field(name=label, value=status, inline=True)
        await ctx.send(embed=embed)

    @antinuke.command(name="enable")
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx):
        if ctx.author.id != ctx.guild.owner_id:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Only the server owner can enable antinuke."
            ))
        await AntinukeConfig.update(self.db, ctx.guild.id, enabled=1)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description="Antinuke has been **enabled**."
        ))

    @antinuke.command(name="disable")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        if ctx.author.id != ctx.guild.owner_id:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Only the server owner can disable antinuke."
            ))
        await AntinukeConfig.update(self.db, ctx.guild.id, enabled=0)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description="Antinuke has been **disabled**."
        ))

    @antinuke.command(name="punishment")
    @commands.has_permissions(administrator=True)
    async def set_punishment(self, ctx, action: str):
        valid = ("ban", "kick", "stripall", "timeout")
        if action.lower() not in valid:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description=f"Valid punishments: {', '.join(valid)}",
            ))
        await AntinukeConfig.update(self.db, ctx.guild.id, punishment=action.lower())
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"Antinuke punishment set to **{action.lower()}**."
        ))

    @antinuke.command(name="whitelist", aliases=["wl"])
    @commands.has_permissions(administrator=True)
    async def whitelist(self, ctx, action: str, member: discord.Member = None):
        if ctx.author.id != ctx.guild.owner_id:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Only the server owner can manage the whitelist."
            ))
        if action == "add" and member:
            await AntinukeConfig.add_whitelist(self.db, ctx.guild.id, member.id, ctx.author.id)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"**{member}** has been whitelisted."
            ))
        elif action == "remove" and member:
            await AntinukeConfig.remove_whitelist(self.db, ctx.guild.id, member.id)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"**{member}** has been removed from the whitelist."
            ))
        elif action == "list":
            rows = await self.db.fetchall(
                "SELECT user_id FROM antinuke_whitelist WHERE guild_id = ?",
                (ctx.guild.id,),
            )
            if not rows:
                return await ctx.send(embed=discord.Embed(
                    color=BOT_COLOR, description="No whitelisted users."
                ))
            entries = [f"<@{r['user_id']}>" for r in rows]
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, title="Whitelisted Users", description="\n".join(entries),
            ))

    @antinuke.command(name="module")
    @commands.has_permissions(administrator=True)
    async def module(self, ctx, name: str, enabled: bool):
        if ctx.author.id != ctx.guild.owner_id:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Only the server owner can configure antinuke modules."
            ))
        valid_modules = {
            "antibot", "antiban", "antikick", "antichannel_create", "antichannel_delete",
            "antichannel_update", "antirole_create", "antirole_delete", "antirole_update",
            "antiwebhook", "antiguild_update", "antieveryone", "antiprune", "antiintegration",
        }
        name = name.lower().replace("-", "_")
        if name not in valid_modules:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR,
                description=f"Valid modules: {', '.join(sorted(valid_modules))}",
            ))
        await AntinukeConfig.update(self.db, ctx.guild.id, **{name: int(enabled)})
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS,
            description=f"**{name}** has been **{'enabled' if enabled else 'disabled'}**.",
        ))

    async def _check_and_punish(self, guild: discord.Guild, user_id: int, action_type: str):
        config = await AntinukeConfig.get(self.db, guild.id)
        if not config.get("enabled"):
            return
        if user_id == guild.owner_id or user_id == self.bot.user.id:
            return
        if await AntinukeConfig.is_whitelisted(self.db, guild.id, user_id):
            return

        await AntinukeConfig.record_action(self.db, guild.id, user_id, action_type)
        threshold_key = f"{action_type.split('_')[0]}_threshold"
        threshold = config.get(threshold_key, 3)
        window = config.get("threshold_window", 10)
        count = await AntinukeConfig.count_recent_actions(
            self.db, guild.id, user_id, action_type, window
        )

        if count >= threshold:
            member = guild.get_member(user_id)
            if not member:
                return
            punishment = config.get("punishment", "ban")
            reason = f"Antinuke: {action_type} threshold exceeded ({count}/{threshold} in {window}s)"
            try:
                if punishment == "ban":
                    await guild.ban(member, reason=reason)
                elif punishment == "kick":
                    await member.kick(reason=reason)
                elif punishment == "stripall":
                    removable = [r for r in member.roles if r != guild.default_role and r < guild.me.top_role]
                    await member.remove_roles(*removable, reason=reason)
                elif punishment == "timeout":
                    import datetime
                    until = discord.utils.utcnow() + datetime.timedelta(hours=24)
                    await member.timeout(until, reason=reason)
            except discord.HTTPException:
                pass

            log_channel_id = config.get("log_channel_id")
            if log_channel_id:
                channel = guild.get_channel(log_channel_id)
                if channel:
                    embed = discord.Embed(
                        color=BOT_COLOR_ERROR,
                        title="Antinuke Triggered",
                        description=f"**User:** {member.mention}\n**Action:** {action_type}\n"
                                    f"**Count:** {count} in {window}s\n**Punishment:** {punishment}",
                    )
                    try:
                        await channel.send(embed=embed)
                    except discord.HTTPException:
                        pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        config = await AntinukeConfig.get(self.db, guild.id)
        if not config.get("antiban"):
            return
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.user.id != self.bot.user.id:
                await self._check_and_punish(guild, entry.user.id, "ban")
            break

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        config = await AntinukeConfig.get(self.db, member.guild.id)
        if not config.get("antikick"):
            return
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id and entry.user.id != self.bot.user.id:
                await self._check_and_punish(member.guild, entry.user.id, "kick")
            break

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        config = await AntinukeConfig.get(self.db, channel.guild.id)
        if not config.get("antichannel_create"):
            return
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
            if entry.user.id != self.bot.user.id:
                await self._check_and_punish(channel.guild, entry.user.id, "channel_create")
            break

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        config = await AntinukeConfig.get(self.db, channel.guild.id)
        if not config.get("antichannel_delete"):
            return
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            if entry.user.id != self.bot.user.id:
                await self._check_and_punish(channel.guild, entry.user.id, "channel_delete")
            break

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        config = await AntinukeConfig.get(self.db, role.guild.id)
        if not config.get("antirole_create"):
            return
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            if entry.user.id != self.bot.user.id:
                await self._check_and_punish(role.guild, entry.user.id, "role_create")
            break

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        config = await AntinukeConfig.get(self.db, role.guild.id)
        if not config.get("antirole_delete"):
            return
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            if entry.user.id != self.bot.user.id:
                await self._check_and_punish(role.guild, entry.user.id, "role_delete")
            break

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel: discord.TextChannel):
        config = await AntinukeConfig.get(self.db, channel.guild.id)
        if not config.get("antiwebhook"):
            return
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create):
            if entry.user.id != self.bot.user.id:
                await self._check_and_punish(channel.guild, entry.user.id, "webhook_create")
            break

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        config = await AntinukeConfig.get(self.db, member.guild.id)
        if not config.get("antibot") or not member.bot:
            return
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
            if entry.target.id == member.id and entry.user.id != member.guild.owner_id:
                if not await AntinukeConfig.is_whitelisted(self.db, member.guild.id, entry.user.id):
                    try:
                        await member.kick(reason="Antinuke: unauthorized bot addition")
                    except discord.HTTPException:
                        pass
                    await self._check_and_punish(member.guild, entry.user.id, "bot_add")
            break


async def setup(bot):
    await bot.add_cog(Antinuke(bot))

