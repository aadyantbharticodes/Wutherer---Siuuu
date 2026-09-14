from __future__ import annotations
import discord
from discord.ext import commands
from typing import Optional

from database.models.onboarding import AutoDMModel
from services.onboarding_service import OnboardingService


class AutoDMCog(commands.Cog, name="Auto DM"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="autodm", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def autodm_group(self, ctx: commands.Context):
        cfg = await AutoDMModel.get(self.bot.db, ctx.guild.id)
        embed = discord.Embed(
            title="✉️ Auto Direct Message On Join",
            color=0x57F287 if cfg.get("enabled") else 0xED4245
        )
        embed.description = f"Status: **{'ENABLED' if cfg.get('enabled') else 'DISABLED'}**\nDelay: **{cfg.get('delay_seconds', 0)}s**"
        embed.add_field(name="Current Message", value=f"```\n{cfg.get('message', '*None*')}\n```", inline=False)
        buttons = cfg.get("buttons", [])
        embed.add_field(name="Action Buttons", value=f"**{len(buttons)}** button(s) configured" if buttons else "*None*", inline=True)
        embed.add_field(name="Commands", value=(
            "`s!autodm toggle` — Enable/disable Auto DM\n"
            "`s!autodm message <text>` — Set custom DM message\n"
            "`s!autodm delay <seconds>` — Delay before sending DM\n"
            "`s!autodm button add <label> <url>` — Add action link button\n"
            "`s!autodm button clear` — Remove all buttons\n"
            "`s!autodm test` — Send a test DM to yourself"
        ), inline=False)
        embed.set_footer(text="Variables: {user}, {user.mention}, {guild.name}, {guild.member_count}")
        await ctx.send(embed=embed)

    @autodm_group.command(name="toggle")
    @commands.has_permissions(manage_guild=True)
    async def autodm_toggle(self, ctx: commands.Context):
        cfg = await AutoDMModel.get(self.bot.db, ctx.guild.id)
        new_state = 0 if cfg.get("enabled") else 1
        await AutoDMModel.update(self.bot.db, ctx.guild.id, enabled=new_state)
        await ctx.send(f"✉️ Auto DM on join is now **{'ENABLED' if new_state else 'DISABLED'}**.")

    @autodm_group.command(name="message")
    @commands.has_permissions(manage_guild=True)
    async def autodm_message(self, ctx: commands.Context, *, text: str):
        await AutoDMModel.update(self.bot.db, ctx.guild.id, message=text)
        await ctx.send(f"✅ Auto DM message updated! Test with `s!autodm test`.")

    @autodm_group.command(name="delay")
    @commands.has_permissions(manage_guild=True)
    async def autodm_delay(self, ctx: commands.Context, seconds: int):
        sec = max(0, min(seconds, 300))
        await AutoDMModel.update(self.bot.db, ctx.guild.id, delay_seconds=sec)
        await ctx.send(f"⏱️ Auto DM delay set to **{sec}** seconds.")

    @autodm_group.group(name="button", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def autodm_button(self, ctx: commands.Context):
        await ctx.send("Usage: `s!autodm button add <label> <url>` or `s!autodm button clear`")

    @autodm_button.command(name="add")
    @commands.has_permissions(manage_guild=True)
    async def autodm_button_add(self, ctx: commands.Context, label: str, url: str):
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("discord://")):
            await ctx.send("❌ URL must start with `http://`, `https://`, or `discord://`.")
            return
        cfg = await AutoDMModel.get(self.bot.db, ctx.guild.id)
        buttons = cfg.get("buttons", [])
        if len(buttons) >= 5:
            await ctx.send("❌ Maximum 5 action buttons allowed.")
            return
        buttons.append({"label": label, "url": url})
        await AutoDMModel.update(self.bot.db, ctx.guild.id, buttons=buttons)
        await ctx.send(f"✅ Added action button: **{label}** -> `<{url}>`")

    @autodm_button.command(name="clear")
    @commands.has_permissions(manage_guild=True)
    async def autodm_button_clear(self, ctx: commands.Context):
        await AutoDMModel.update(self.bot.db, ctx.guild.id, buttons=[])
        await ctx.send("🗑️ Cleared all Auto DM action buttons.")

    @autodm_group.command(name="test")
    async def autodm_test(self, ctx: commands.Context):
        sent = await OnboardingService.dispatch_auto_dm(self.bot, self.bot.db, ctx.author)
        if sent:
            await ctx.send("📬 Sent test Auto DM to your direct messages!")
        else:
            await ctx.send("❌ Could not send test DM. Please check your privacy settings or enable Auto DM first.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        await OnboardingService.dispatch_auto_dm(self.bot, self.bot.db, member)


async def setup(bot):
    await bot.add_cog(AutoDMCog(bot))
