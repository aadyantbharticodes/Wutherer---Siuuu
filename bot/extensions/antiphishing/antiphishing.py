from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

import discord
from discord.ext import commands

from bot.core.cog import WuthererCog
from bot.core.context import WuthererContext
from bot.core.checks import is_admin
from bot.services.antiphishing import AntiPhishingService
from bot.database.models.antiphishing import AntiPhishingModel, AntiPhishingConfig

if TYPE_CHECKING:
    from bot.core.bot import WuthererBot


class AntiPhishing(WuthererCog, name="AntiPhishing"):

    def __init__(self, bot: WuthererBot) -> None:
        super().__init__(bot)

    @WuthererCog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not message.guild or not isinstance(message.author, discord.Member):
            return


        if message.author.guild_permissions.administrator:
            return

        urls = AntiPhishingService.extract_urls(message.content)
        if not urls:
            return

        if not self.bot.db_pool:
            return

        async with self.bot.db_pool.acquire() as db:
            dao = AntiPhishingModel(db)
            config = await dao.get_config(message.guild.id)

        if not config.enabled:
            return

        for url in urls:
            is_malicious, reason = AntiPhishingService.evaluate_url(
                url,
                whitelisted_domains=config.whitelisted_domains,
                custom_blacklist=config.custom_blacklisted_domains,
            )

            if is_malicious:
                await self._handle_phishing_violation(message, url, reason, config)
                break

    async def _handle_phishing_violation(
        self,
        message: discord.Message,
        url: str,
        reason: str,
        config: AntiPhishingConfig,
    ) -> None:
        member = message.author
        guild = message.guild


        try:
            await message.delete()
        except discord.HTTPException:
            pass


        punishment_str = "Deleted Message"
        if config.action == "timeout":
            try:
                until = discord.utils.utcnow() + datetime.timedelta(seconds=config.timeout_duration)
                await member.timeout(until, reason=f"Sentinel Phishing Protection: {reason}")
                punishment_str = f"Timed out for {config.timeout_duration // 60} minutes"
            except discord.HTTPException:
                pass
        elif config.action == "kick":
            try:
                await member.kick(reason=f"Sentinel Phishing Protection: {reason}")
                punishment_str = "Kicked from server"
            except discord.HTTPException:
                pass
        elif config.action == "ban":
            try:
                await member.ban(reason=f"Sentinel Phishing Protection: {reason}", delete_message_days=1)
                punishment_str = "Permanently Banned"
            except discord.HTTPException:
                pass


        try:
            dm_embed = self.bot.embed.create(
                title="⚠️ Security Alert — Suspicious Link Intercepted",
                description=(
                    f"A link you posted in **{guild.name}** was flagged as a potential phishing or scam URL:\n"
                    f"`{url}`\n\n"
                    f"**Reason:** {reason}\n"
                    f"**Action Taken:** {punishment_str}\n\n"
                    "If you did not send this, **your account or Discord token may be compromised**. "
                    "Change your Discord password immediately and enable Two-Factor Authentication (2FA)."
                ),
                color=self.bot.embed.COLOR_DANGER,
            )
            await member.send(embed=dm_embed)
        except discord.HTTPException:
            pass


        if config.log_channel_id:
            log_ch = guild.get_channel(config.log_channel_id)
            if log_ch and isinstance(log_ch, discord.TextChannel):
                alert_embed = self.bot.embed.create(
                    title="🚨 Anti-Phishing Interception",
                    description=f"Sentinel neutralized a scam link posted by {member.mention}.",
                    color=self.bot.embed.COLOR_DANGER,
                )
                alert_embed.add_field(name="User", value=f"{member} (`{member.id}`)", inline=True)
                alert_embed.add_field(name="Channel", value=message.channel.mention, inline=True)
                alert_embed.add_field(name="Action Taken", value=punishment_str, inline=True)
                alert_embed.add_field(name="Flagged URL", value=f"`{url}`", inline=False)
                alert_embed.add_field(name="Detection Reason", value=reason, inline=False)
                await log_ch.send(embed=alert_embed)

    @commands.group(name="antiphishing", aliases=["phishguard", "linkshield"], invoke_without_command=True)
    @is_admin()
    async def ap_group(self, ctx: WuthererContext) -> None:
        await ctx.send_help(ctx.command)

    @ap_group.command(name="enable")
    @is_admin()
    async def ap_enable(self, ctx: WuthererContext) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = AntiPhishingModel(db)
            cfg = await dao.get_config(ctx.guild.id)
            cfg.enabled = True
            await dao.save_config(cfg)
        await ctx.send_success("Anti-phishing security scanner is now **Enabled**.")

    @ap_group.command(name="disable")
    @is_admin()
    async def ap_disable(self, ctx: WuthererContext) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = AntiPhishingModel(db)
            cfg = await dao.get_config(ctx.guild.id)
            cfg.enabled = False
            await dao.save_config(cfg)
        await ctx.send_warn("Anti-phishing scanner is now **Disabled**.")

    @ap_group.command(name="action")
    @is_admin()
    async def ap_action(self, ctx: WuthererContext, action: str) -> None:
        action = action.lower()
        if action not in ["delete", "timeout", "kick", "ban"]:
            await ctx.send_error("Invalid action. Choose from: `delete`, `timeout`, `kick`, `ban`.")
            return

        async with self.bot.db_pool.acquire() as db:
            dao = AntiPhishingModel(db)
            cfg = await dao.get_config(ctx.guild.id)
            cfg.action = action
            await dao.save_config(cfg)

        await ctx.send_success(f"Anti-phishing violation action set to **`{action.upper()}`**.")

    @ap_group.command(name="scan")
    async def ap_scan(self, ctx: WuthererContext, url: str) -> None:
        is_malicious, reason = AntiPhishingService.evaluate_url(url)
        domain = AntiPhishingService.extract_domain(url)

        embed = self.bot.embed.create(
            title="🔍 URL Reputation Audit",
            description=f"Scanned target: `{url}`",
            color=self.bot.embed.COLOR_DANGER if is_malicious else self.bot.embed.COLOR_SUCCESS,
        )
        embed.add_field(name="Extracted Domain", value=f"`{domain}`", inline=True)
        embed.add_field(name="Verdict", value="🚨 **MALICIOUS / PHISHING**" if is_malicious else "✅ **SAFE / CLEAN**", inline=True)
        embed.add_field(name="Analysis Notes", value=reason, inline=False)

        await ctx.send(embed=embed)


async def setup(bot: WuthererBot) -> None:
    await bot.add_cog(AntiPhishing(bot))

