from __future__ import annotations
import json
import re
from collections import defaultdict
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_COLOR, BOT_COLOR_WARNING
from database.models.moderation import AutomodConfig


class Automod(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self._spam_tracker: dict[int, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
        self._invite_pattern = re.compile(
            r"(?:https?://)?(?:www\.)?(?:discord\.(?:gg|io|me|li)|discordapp\.com/invite)/[a-zA-Z0-9]+",
            re.IGNORECASE,
        )
        self._url_pattern = re.compile(
            r"https?://[^\s<>\"]+|www\.[^\s<>\"]+", re.IGNORECASE
        )

    @commands.group(name="automod", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def automod(self, ctx):
        config = await AutomodConfig.get(self.db, ctx.guild.id)
        embed = discord.Embed(color=BOT_COLOR, title="Automod Configuration")
        embed.add_field(name="Anti-Spam", value="Enabled" if config.get("antispam") else "Disabled", inline=True)
        embed.add_field(name="Anti-Caps", value="Enabled" if config.get("anticaps") else "Disabled", inline=True)
        embed.add_field(name="Anti-Link", value="Enabled" if config.get("antilink") else "Disabled", inline=True)
        embed.add_field(name="Anti-Invite", value="Enabled" if config.get("antiinvite") else "Disabled", inline=True)
        embed.add_field(name="Anti-Mention", value="Enabled" if config.get("antimention") else "Disabled", inline=True)
        embed.add_field(name="Anti-Emoji", value="Enabled" if config.get("antiemoji") else "Disabled", inline=True)
        punishment = config.get("punishment", "delete")
        embed.add_field(name="Punishment", value=punishment.capitalize(), inline=True)
        badwords = config.get("badwords", [])
        if isinstance(badwords, str):
            badwords = json.loads(badwords) if badwords else []
        embed.add_field(name="Bad Words", value=str(len(badwords)), inline=True)
        await ctx.send(embed=embed)

    @automod.command(name="antispam")
    @commands.has_permissions(manage_guild=True)
    async def antispam(self, ctx, enabled: bool, threshold: int = 5, interval: int = 5):
        await AutomodConfig.update(
            self.db, ctx.guild.id,
            antispam=int(enabled), antispam_threshold=threshold, antispam_interval=interval,
        )
        status = "enabled" if enabled else "disabled"
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR, description=f"Anti-spam **{status}** (threshold: {threshold} messages in {interval}s)."
        ))

    @automod.command(name="anticaps")
    @commands.has_permissions(manage_guild=True)
    async def anticaps(self, ctx, enabled: bool, threshold: int = 70, min_length: int = 10):
        await AutomodConfig.update(
            self.db, ctx.guild.id,
            anticaps=int(enabled), anticaps_threshold=threshold, anticaps_min_length=min_length,
        )
        status = "enabled" if enabled else "disabled"
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR, description=f"Anti-caps **{status}** ({threshold}% threshold, min {min_length} chars)."
        ))

    @automod.command(name="antilink")
    @commands.has_permissions(manage_guild=True)
    async def antilink(self, ctx, enabled: bool):
        await AutomodConfig.update(self.db, ctx.guild.id, antilink=int(enabled))
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR, description=f"Anti-link **{'enabled' if enabled else 'disabled'}**."
        ))

    @automod.command(name="antiinvite")
    @commands.has_permissions(manage_guild=True)
    async def antiinvite(self, ctx, enabled: bool):
        await AutomodConfig.update(self.db, ctx.guild.id, antiinvite=int(enabled))
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR, description=f"Anti-invite **{'enabled' if enabled else 'disabled'}**."
        ))

    @automod.command(name="antimention")
    @commands.has_permissions(manage_guild=True)
    async def antimention(self, ctx, enabled: bool, threshold: int = 5):
        await AutomodConfig.update(
            self.db, ctx.guild.id, antimention=int(enabled), antimention_threshold=threshold,
        )
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR, description=f"Anti-mention **{'enabled' if enabled else 'disabled'}** (threshold: {threshold})."
        ))

    @automod.command(name="antiemoji")
    @commands.has_permissions(manage_guild=True)
    async def antiemoji_cmd(self, ctx, enabled: bool, threshold: int = 10):
        await AutomodConfig.update(
            self.db, ctx.guild.id, antiemoji=int(enabled), antiemoji_threshold=threshold,
        )
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR, description=f"Anti-emoji **{'enabled' if enabled else 'disabled'}** (threshold: {threshold})."
        ))

    @automod.command(name="punishment")
    @commands.has_permissions(manage_guild=True)
    async def punishment(self, ctx, action: str):
        valid = ("delete", "warn", "timeout", "kick", "ban")
        if action.lower() not in valid:
            return await ctx.send(embed=discord.Embed(
                color=BOT_COLOR_WARNING,
                description=f"Valid punishments: {', '.join(valid)}",
            ))
        await AutomodConfig.update(self.db, ctx.guild.id, punishment=action.lower())
        await ctx.send(embed=discord.Embed(
            color=BOT_COLOR, description=f"Automod punishment set to **{action.lower()}**."
        ))

    @automod.command(name="badword")
    @commands.has_permissions(manage_guild=True)
    async def badword(self, ctx, action: str, *, word: str = None):
        config = await AutomodConfig.get(self.db, ctx.guild.id)
        badwords = config.get("badwords", [])
        if isinstance(badwords, str):
            badwords = json.loads(badwords) if badwords else []

        if action == "add" and word:
            if word.lower() not in badwords:
                badwords.append(word.lower())
                await AutomodConfig.update(self.db, ctx.guild.id, badwords=badwords)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description=f"Added **{word}** to bad words list."
            ))
        elif action == "remove" and word:
            if word.lower() in badwords:
                badwords.remove(word.lower())
                await AutomodConfig.update(self.db, ctx.guild.id, badwords=badwords)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description=f"Removed **{word}** from bad words list."
            ))
        elif action == "list":
            if not badwords:
                return await ctx.send(embed=discord.Embed(
                    color=BOT_COLOR, description="No bad words configured."
                ))
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR,
                title="Bad Words",
                description=", ".join(f"`{w}`" for w in badwords),
            ))
        elif action == "clear":
            await AutomodConfig.update(self.db, ctx.guild.id, badwords=[])
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description="Cleared all bad words."
            ))

    @automod.command(name="ignore")
    @commands.has_permissions(manage_guild=True)
    async def ignore(self, ctx, target: str, obj: discord.abc.GuildChannel | discord.Role = None):
        config = await AutomodConfig.get(self.db, ctx.guild.id)
        if target == "channel" and isinstance(obj, discord.abc.GuildChannel):
            ignored = config.get("ignored_channels", [])
            if obj.id not in ignored:
                ignored.append(obj.id)
                await AutomodConfig.update(self.db, ctx.guild.id, ignored_channels=ignored)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description=f"{obj.mention} will be ignored by automod."
            ))
        elif target == "role" and isinstance(obj, discord.Role):
            ignored = config.get("ignored_roles", [])
            if obj.id not in ignored:
                ignored.append(obj.id)
                await AutomodConfig.update(self.db, ctx.guild.id, ignored_roles=ignored)
            await ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description=f"**{obj.name}** will be ignored by automod."
            ))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild or message.author.bot:
            return
        if message.author.guild_permissions.manage_messages:
            return

        config = await AutomodConfig.get(self.db, message.guild.id)
        if not config or config.get("guild_id") is None:
            return

        ignored_channels = config.get("ignored_channels", [])
        if message.channel.id in ignored_channels:
            return
        ignored_roles = config.get("ignored_roles", [])
        if any(r.id in ignored_roles for r in message.author.roles):
            return

        violations = []

        if config.get("antispam"):
            if await self._check_spam(message, config):
                violations.append("spam")

        if config.get("anticaps") and len(message.content) >= config.get("anticaps_min_length", 10):
            upper = sum(1 for c in message.content if c.isupper())
            ratio = (upper / len(message.content)) * 100
            if ratio >= config.get("anticaps_threshold", 70):
                violations.append("excessive caps")

        if config.get("antilink") and self._url_pattern.search(message.content):
            whitelist = config.get("antilink_whitelist", [])
            if not any(domain in message.content for domain in whitelist):
                violations.append("links")

        if config.get("antiinvite") and self._invite_pattern.search(message.content):
            violations.append("discord invite")

        if config.get("antimention"):
            mention_count = len(message.mentions) + len(message.role_mentions)
            if mention_count >= config.get("antimention_threshold", 5):
                violations.append("mass mentions")

        if config.get("antiemoji"):
            emoji_count = len(re.findall(r"<a?:\w+:\d+>|[\U0001f000-\U0001ffff]", message.content))
            if emoji_count >= config.get("antiemoji_threshold", 10):
                violations.append("excessive emojis")

        badwords = config.get("badwords", [])
        if badwords:
            content_lower = message.content.lower()
            if any(word in content_lower for word in badwords):
                violations.append("bad word")

        if violations:
            await self._handle_violation(message, config, violations)

    async def _check_spam(self, message: discord.Message, config: dict) -> bool:
        import time
        now = time.time()
        guild_id = message.guild.id
        user_id = message.author.id
        interval = config.get("antispam_interval", 5)
        threshold = config.get("antispam_threshold", 5)

        self._spam_tracker[guild_id][user_id] = [
            t for t in self._spam_tracker[guild_id][user_id] if now - t < interval
        ]
        self._spam_tracker[guild_id][user_id].append(now)
        return len(self._spam_tracker[guild_id][user_id]) >= threshold

    async def _handle_violation(self, message: discord.Message, config: dict, violations: list[str]):
        try:
            await message.delete()
        except discord.HTTPException:
            pass

        punishment = config.get("punishment", "delete")
        reason = f"Automod: {', '.join(violations)}"

        if punishment == "warn":
            from database.models.moderation import ModerationDB
            await ModerationDB.add_warning(
                self.db, message.guild.id, message.author.id,
                self.bot.user.id, reason,
            )
            try:
                await message.channel.send(
                    f"{message.author.mention}, your message was removed ({reason}).",
                    delete_after=5,
                )
            except discord.HTTPException:
                pass
        elif punishment == "timeout":
            import datetime
            try:
                until = discord.utils.utcnow() + datetime.timedelta(minutes=5)
                await message.author.timeout(until, reason=reason)
            except discord.HTTPException:
                pass
        elif punishment == "kick":
            try:
                await message.author.kick(reason=reason)
            except discord.HTTPException:
                pass
        elif punishment == "ban":
            try:
                await message.guild.ban(message.author, reason=reason)
            except discord.HTTPException:
                pass

        log_channel_id = config.get("log_channel_id")
        if log_channel_id:
            channel = message.guild.get_channel(log_channel_id)
            if channel:
                embed = discord.Embed(
                    color=BOT_COLOR_WARNING,
                    title="Automod Action",
                    description=f"**User:** {message.author.mention}\n"
                                f"**Channel:** {message.channel.mention}\n"
                                f"**Violation:** {', '.join(violations)}\n"
                                f"**Action:** {punishment}\n"
                                f"**Content:** {message.content[:200]}",
                )
                try:
                    await channel.send(embed=embed)
                except discord.HTTPException:
                    pass


async def setup(bot):
    await bot.add_cog(Automod(bot))

