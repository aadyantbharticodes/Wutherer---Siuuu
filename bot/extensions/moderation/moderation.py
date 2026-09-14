from __future__ import annotations
import datetime
from typing import Optional, Union

import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_mod, can_moderate, bot_has_permissions
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR, BOT_COLOR_WARNING
from database.models.moderation import ModerationDB


class Moderation(WuthererCog):

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: Union[discord.Member, discord.User], *, reason: str = "No reason provided"):
        if isinstance(member, discord.Member) and not can_moderate(member, ctx.author, ctx.guild):
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description=f"Cannot ban {member.mention} — role hierarchy prevents this."
            ))
        await ctx.guild.ban(member, reason=f"{ctx.author} | {reason}", delete_message_days=0)
        case_id = await ModerationDB.add_case(self.db, ctx.guild.id, member.id, ctx.author.id, "ban", reason)
        embed = discord.Embed(color=BOT_COLOR_SUCCESS, description=f"**{member}** has been banned.\n**Reason:** {reason}\n**Case:** #{case_id}")
        await ctx.send(embed=embed)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason: str = "No reason provided"):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"{ctx.author} | {reason}")
            case_id = await ModerationDB.add_case(self.db, ctx.guild.id, user.id, ctx.author.id, "unban", reason)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"**{user}** has been unbanned.\n**Case:** #{case_id}"
            ))
        except discord.NotFound:
            await ctx.send(embed=discord.Embed(color=BOT_COLOR_ERROR, description="User not found or not banned."))

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if not can_moderate(member, ctx.author, ctx.guild):
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description=f"Cannot kick {member.mention} — role hierarchy prevents this."
            ))
        try:
            await member.send(embed=discord.Embed(
                color=BOT_COLOR_WARNING,
                description=f"You have been kicked from **{ctx.guild.name}**.\n**Reason:** {reason}",
            ))
        except discord.HTTPException:
            pass
        await member.kick(reason=f"{ctx.author} | {reason}")
        case_id = await ModerationDB.add_case(self.db, ctx.guild.id, member.id, ctx.author.id, "kick", reason)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"**{member}** has been kicked.\n**Reason:** {reason}\n**Case:** #{case_id}"
        ))

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if not can_moderate(member, ctx.author, ctx.guild):
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Cannot warn this user — role hierarchy prevents this."
            ))
        warn_id = await ModerationDB.add_warning(self.db, ctx.guild.id, member.id, ctx.author.id, reason)
        count = await ModerationDB.count_warnings(self.db, ctx.guild.id, member.id)
        await ModerationDB.add_case(self.db, ctx.guild.id, member.id, ctx.author.id, "warn", reason)

        try:
            await member.send(embed=discord.Embed(
                color=BOT_COLOR_WARNING,
                description=f"You have been warned in **{ctx.guild.name}**.\n**Reason:** {reason}\n**Warning #{count}**",
            ))
        except discord.HTTPException:
            pass

        embed = discord.Embed(
            color=BOT_COLOR_SUCCESS,
            description=f"**{member}** has been warned.\n**Reason:** {reason}\n**Warning #{count}** (ID: {warn_id})",
        )
        await ctx.send(embed=embed)

        from config import MAX_WARNS
        if count >= MAX_WARNS:
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_WARNING,
                description=f"{member.mention} has reached **{count}** warnings. Consider further action.",
            ))

    @commands.command(name="warnings", aliases=["warns"])
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        warns = await ModerationDB.get_warnings(self.db, ctx.guild.id, member.id)
        if not warns:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description=f"**{member}** has no warnings."
            ))
        entries = []
        for w in warns:
            entries.append(f"**#{w['id']}** — {w['reason'] or 'No reason'} (by <@{w['moderator_id']}>) — {w['created_at']}")
        await ctx.paginate(entries, per_page=5, title=f"Warnings for {member}")

    @commands.command(name="clearwarns")
    @commands.has_permissions(manage_guild=True)
    async def clearwarns(self, ctx, member: discord.Member):
        count = await ModerationDB.clear_warnings(self.db, ctx.guild.id, member.id)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"Cleared **{count}** warnings from **{member}**."
        ))

    @commands.command(name="delwarn")
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, warn_id: int):
        removed = await ModerationDB.remove_warning(self.db, warn_id)
        if removed:
            await ctx.send(embed=discord.Embed(color=BOT_COLOR_SUCCESS, description=f"Warning #{warn_id} removed."))
        else:
            await ctx.send(embed=discord.Embed(color=BOT_COLOR_ERROR, description="Warning not found."))

    @commands.command(name="timeout", aliases=["mute"])
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout_cmd(self, ctx, member: discord.Member, duration: str = "10m", *, reason: str = "No reason provided"):
        if not can_moderate(member, ctx.author, ctx.guild):
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Cannot timeout this user — role hierarchy prevents this."
            ))
        seconds = self._parse_duration(duration)
        if not seconds or seconds > 2419200:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Invalid duration. Use formats like 10s, 5m, 1h, 1d (max 28 days)."
            ))
        until = discord.utils.utcnow() + datetime.timedelta(seconds=seconds)
        await member.timeout(until, reason=f"{ctx.author} | {reason}")
        case_id = await ModerationDB.add_case(self.db, ctx.guild.id, member.id, ctx.author.id, "timeout", reason, seconds)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS,
            description=f"**{member}** has been timed out for **{duration}**.\n**Reason:** {reason}\n**Case:** #{case_id}",
        ))

    @commands.command(name="untimeout", aliases=["unmute"])
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.timeout(None, reason=f"{ctx.author} | {reason}")
        await ModerationDB.add_case(self.db, ctx.guild.id, member.id, ctx.author.id, "untimeout", reason)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"**{member}** has been untimeouted."
        ))

    @commands.command(name="softban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if not can_moderate(member, ctx.author, ctx.guild):
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Cannot softban this user."
            ))
        await ctx.guild.ban(member, reason=f"Softban by {ctx.author} | {reason}", delete_message_days=7)
        await ctx.guild.unban(member, reason="Softban completion")
        case_id = await ModerationDB.add_case(self.db, ctx.guild.id, member.id, ctx.author.id, "softban", reason)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS,
            description=f"**{member}** has been softbanned (messages deleted, user kicked).\n**Case:** #{case_id}",
        ))

    @commands.command(name="purge", aliases=["clear", "clean"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10, member: discord.Member = None):
        if amount < 1 or amount > 500:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Amount must be between 1 and 500."
            ))
        def check(m):
            if member:
                return m.author.id == member.id
            return True
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount, check=check)
        msg = await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"Deleted **{len(deleted)}** messages."
        ))
        await msg.delete(delay=3)

    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, *, reason: str = "No reason provided"):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=reason)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"{channel.mention} has been locked."
        ))

    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None, *, reason: str = "No reason provided"):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=reason)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"{channel.mention} has been unlocked."
        ))

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        if seconds < 0 or seconds > 21600:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Slowmode must be between 0 and 21600 seconds (6 hours)."
            ))
        await channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"Slowmode disabled in {channel.mention}."
            ))
        else:
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"Slowmode set to **{seconds}s** in {channel.mention}."
            ))

    @commands.command(name="nuke")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        confirmed = await ctx.confirm(
            f"This will clone and delete {channel.mention}, wiping all messages. Continue?"
        )
        if not confirmed:
            return await ctx.send(embed=discord.Embed(color=BOT_COLOR, description="Cancelled."))
        new_channel = await channel.clone(reason=f"Nuked by {ctx.author}")
        await new_channel.edit(position=channel.position)
        await channel.delete(reason=f"Nuked by {ctx.author}")
        await new_channel.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description="Channel has been nuked."
        ))

    @commands.command(name="modlog", aliases=["cases", "history"])
    @commands.has_permissions(manage_messages=True)
    async def modlog(self, ctx, member: discord.Member = None, limit: int = 20):
        cases = await ModerationDB.get_cases(self.db, ctx.guild.id, member.id if member else None, limit)
        if not cases:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description="No moderation cases found."
            ))
        entries = []
        for c in cases:
            entries.append(
                f"**#{c['id']}** [{c['action'].upper()}] <@{c['user_id']}> by <@{c['moderator_id']}> — "
                f"{c['reason'] or 'No reason'} — {c['created_at']}"
            )
        title = f"Mod log for {member}" if member else "Server mod log"
        await ctx.paginate(entries, per_page=5, title=title)

    @commands.command(name="note")
    @commands.has_permissions(manage_messages=True)
    async def note(self, ctx, member: discord.Member, *, content: str):
        note_id = await ModerationDB.add_note(self.db, ctx.guild.id, member.id, ctx.author.id, content)
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"Note #{note_id} added for **{member}**."
        ))

    @commands.command(name="notes")
    @commands.has_permissions(manage_messages=True)
    async def notes(self, ctx, member: discord.Member):
        notes = await ModerationDB.get_notes(self.db, ctx.guild.id, member.id)
        if not notes:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description=f"No notes for **{member}**."
            ))
        entries = []
        for n in notes:
            entries.append(f"**#{n['id']}** — {n['content']} (by <@{n['moderator_id']}>) — {n['created_at']}")
        await ctx.paginate(entries, per_page=5, title=f"Notes for {member}")

    @commands.command(name="massban")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(ban_members=True)
    async def massban(self, ctx, *user_ids: int):
        if not user_ids:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Provide user IDs to ban."
            ))
        if len(user_ids) > 50:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Maximum 50 users per massban."
            ))
        confirmed = await ctx.confirm(f"Ban **{len(user_ids)}** users?")
        if not confirmed:
            return
        banned = 0
        for uid in user_ids:
            try:
                user = discord.Object(id=uid)
                await ctx.guild.ban(user, reason=f"Massban by {ctx.author}")
                banned += 1
            except Exception:
                continue
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"Banned **{banned}/{len(user_ids)}** users."
        ))

    @commands.command(name="role")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, role: discord.Role, *, reason: str = None):
        if role >= ctx.guild.me.top_role:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="I cannot manage that role — it's above my highest role."
            ))
        if role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="That role is above your highest role."
            ))
        if role in member.roles:
            await member.remove_roles(role, reason=reason)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"Removed **{role.name}** from **{member}**."
            ))
        else:
            await member.add_roles(role, reason=reason)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"Added **{role.name}** to **{member}**."
            ))

    @commands.command(name="roleall")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def roleall(self, ctx, role: discord.Role, target: str = "humans"):
        if role >= ctx.guild.me.top_role:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Cannot assign a role above my top role."
            ))
        members = ctx.guild.members
        if target == "humans":
            members = [m for m in members if not m.bot]
        elif target == "bots":
            members = [m for m in members if m.bot]
        confirmed = await ctx.confirm(f"Add **{role.name}** to **{len(members)}** members?")
        if not confirmed:
            return
        added = 0
        for member in members:
            if role not in member.roles:
                try:
                    await member.add_roles(role, reason=f"Roleall by {ctx.author}")
                    added += 1
                except Exception:
                    continue
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"Added **{role.name}** to **{added}** members."
        ))

    @commands.command(name="nickname", aliases=["nick"])
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, name: str = None):
        if not can_moderate(member, ctx.author, ctx.guild):
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Cannot change this user's nickname."
            ))
        await member.edit(nick=name)
        if name:
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"Nickname of **{member}** changed to **{name}**."
            ))
        else:
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_SUCCESS, description=f"Nickname of **{member}** has been reset."
            ))

    @commands.command(name="stripall")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def stripall(self, ctx, member: discord.Member):
        if not can_moderate(member, ctx.author, ctx.guild):
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_ERROR, description="Cannot strip roles from this user."
            ))
        confirmed = await ctx.confirm(f"Remove all roles from **{member}**?")
        if not confirmed:
            return
        removable = [r for r in member.roles if r != ctx.guild.default_role and r < ctx.guild.me.top_role]
        await member.remove_roles(*removable, reason=f"Strip all by {ctx.author}")
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR_SUCCESS, description=f"Removed **{len(removable)}** roles from **{member}**."
        ))

    @staticmethod
    def _parse_duration(text: str) -> Optional[int]:
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        text = text.lower().strip()
        if not text:
            return None
        if text[-1] in units:
            try:
                return int(text[:-1]) * units[text[-1]]
            except ValueError:
                return None
        try:
            return int(text)
        except ValueError:
            return None


async def setup(bot):
    await bot.add_cog(Moderation(bot))

