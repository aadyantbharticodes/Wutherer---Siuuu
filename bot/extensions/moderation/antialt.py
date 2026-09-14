from __future__ import annotations
import discord
from discord.ext import commands
from typing import Optional

from database.models.antialt import AntiAltModel
from services.antialt import AntiAltService


class AntiAltCog(commands.Cog, name="Anti-Alt"):
    def __init__(self, bot):
        self.bot = bot
        self.service = AntiAltService(bot, bot.db)

    @commands.group(name="antialt", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def antialt_group(self, ctx: commands.Context):
        cfg = await AntiAltModel.get_config(self.bot.db, ctx.guild.id)
        embed = discord.Embed(
            title="🛡️ Anti-Alt & Account Verification Shield",
            color=0x57F287 if cfg.get("enabled") else 0xED4245
        )
        embed.description = f"Status: **{'ENABLED' if cfg.get('enabled') else 'DISABLED'}**\nAction: **{cfg.get('action_type', 'quarantine').upper()}**"
        embed.add_field(name="Minimum Account Age", value=f"**{cfg.get('min_age_days', 7)}** days", inline=True)
        embed.add_field(name="Require Custom Avatar", value="**YES**" if cfg.get("require_avatar") else "**NO**", inline=True)
        embed.add_field(name="Commands", value=(
            "`s!antialt toggle` — Enable/disable anti-alt filter\n"
            "`s!antialt minage <days>` — Set minimum account age\n"
            "`s!antialt avatar <on/off>` — Require custom avatar\n"
            "`s!antialt action <quarantine/kick/ban>` — Set automated penalty\n"
            "`s!antialt logs` — View recent flagged accounts"
        ), inline=False)
        embed.set_footer(text="Protects against raid alts, burner accounts, and bot waves")
        await ctx.send(embed=embed)

    @antialt_group.command(name="toggle")
    @commands.has_permissions(administrator=True)
    async def antialt_toggle(self, ctx: commands.Context):
        cfg = await AntiAltModel.get_config(self.bot.db, ctx.guild.id)
        new_state = 0 if cfg.get("enabled") else 1
        await AntiAltModel.update_config(self.bot.db, ctx.guild.id, enabled=new_state)
        await ctx.send(f"🛡️ Anti-Alt Shield is now **{'ENABLED' if new_state else 'DISABLED'}**.")

    @antialt_group.command(name="minage")
    @commands.has_permissions(administrator=True)
    async def antialt_minage(self, ctx: commands.Context, days: int):
        d = max(1, min(days, 365))
        await AntiAltModel.update_config(self.bot.db, ctx.guild.id, min_age_days=d)
        await ctx.send(f"⏱️ Minimum account age set to **{d}** day(s).")

    @antialt_group.command(name="avatar")
    @commands.has_permissions(administrator=True)
    async def antialt_avatar(self, ctx: commands.Context, state: str):
        enable = 1 if state.lower() in ("on", "enable", "yes", "true", "1") else 0
        await AntiAltModel.update_config(self.bot.db, ctx.guild.id, require_avatar=enable)
        await ctx.send(f"🖼️ Custom avatar requirement is now **{'ENABLED' if enable else 'DISABLED'}**.")

    @antialt_group.command(name="action")
    @commands.has_permissions(administrator=True)
    async def antialt_action(self, ctx: commands.Context, action: str):
        act = action.lower()
        if act not in ("quarantine", "kick", "ban"):
            await ctx.send("❌ Action must be `quarantine`, `kick`, or `ban`.")
            return
        await AntiAltModel.update_config(self.bot.db, ctx.guild.id, action_type=act)
        await ctx.send(f"⚖️ Anti-Alt penalty action updated to **{act.upper()}**.")

    @antialt_group.command(name="logs")
    @commands.has_permissions(administrator=True)
    async def antialt_logs(self, ctx: commands.Context):
        logs = await AntiAltModel.get_logs(self.bot.db, ctx.guild.id, limit=8)
        if not logs:
            await ctx.send("ℹ️ No anti-alt violations recorded.")
            return

        embed = discord.Embed(title="🛡️ Anti-Alt Flagged Accounts", color=0xED4245)
        for log in logs:
            embed.add_field(
                name=f"User ID: {log['user_id']} ({log['account_age_days']}d old)",
                value=f"Action: **{log['action_taken']}**\nReason: {log['reason']}\n`{log['created_at']}`",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.service.verify_member(member)


async def setup(bot):
    await bot.add_cog(AntiAltCog(bot))
