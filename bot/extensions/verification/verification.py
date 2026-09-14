from __future__ import annotations
import io
import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_admin
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR
from database.models.verification import VerificationConfig
from services.captcha import CaptchaService


class CaptchaModal(discord.ui.Modal, title="Server Verification"):
    def __init__(self, bot, code: str, role_id: int):
        super().__init__()
        self.bot = bot
        self.solution = code
        self.role_id = role_id

        self.answer_input = discord.ui.TextInput(
            label="Enter CAPTCHA Code",
            placeholder="Type the 5 characters shown in the image...",
            min_length=3,
            max_length=8,
            required=True
        )
        self.add_item(self.answer_input)

    async def on_submit(self, interaction: discord.Interaction):
        user_answer = self.answer_input.value.strip().upper()
        if user_answer == self.solution.upper():
            role = interaction.guild.get_role(self.role_id)
            if role and interaction.guild.me.guild_permissions.manage_roles and role < interaction.guild.me.top_role:
                try:
                    await interaction.user.add_roles(role, reason="Sentinel Verification Passed")
                except discord.HTTPException:
                    pass
            await VerificationConfig.record_attempt(self.bot.db, interaction.guild.id, interaction.user.id, True)
            await interaction.response.send_message("✅ **Verification successful!** Welcome to the server.", ephemeral=True)
        else:
            await VerificationConfig.record_attempt(self.bot.db, interaction.guild.id, interaction.user.id, False)
            await interaction.response.send_message("❌ **Incorrect code.** Please click the button to try a new CAPTCHA.", ephemeral=True)


class VerifyButtonView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="🛡️ Verify Here", style=discord.ButtonStyle.success, custom_id="sentinel_verify_btn")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        cfg = await VerificationConfig.get(self.bot.db, interaction.guild.id)
        if not cfg.get("enabled"):
            return await interaction.response.send_message("Verification is not currently active.", ephemeral=True)

        role_id = cfg.get("role_id")
        if not role_id:
            return await interaction.response.send_message("Verified role is not configured.", ephemeral=True)

        role = interaction.guild.get_role(role_id)
        if role and role in interaction.user.roles:
            return await interaction.response.send_message("You are already verified in this server.", ephemeral=True)

        code, img_buffer = CaptchaService.generate_text_captcha(length=5, difficulty=cfg.get("difficulty", "medium"))
        file = discord.File(img_buffer, filename="captcha.png")


        await interaction.response.send_modal(CaptchaModal(self.bot, code, role_id))


class Verification(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot.add_view(VerifyButtonView(self.bot))

    @commands.group(name="verification", aliases=["verifyconfig"], invoke_without_command=True)
    @is_admin()
    async def verify_group(self, ctx: commands.Context):
        cfg = await VerificationConfig.get(self.bot.db, ctx.guild.id)
        role = ctx.guild.get_role(cfg.get("role_id")) if cfg.get("role_id") else None
        embed = discord.Embed(
            title="🛡️ Server Verification Status",
            color=BOT_COLOR
        )
        embed.add_field(name="Status", value="Enabled" if cfg.get("enabled") else "Disabled", inline=True)
        embed.add_field(name="Verified Role", value=role.mention if role else "Not set", inline=True)
        embed.add_field(name="Difficulty", value=cfg.get("difficulty", "medium").title(), inline=True)
        await ctx.send(embed=embed)

    @verify_group.command(name="setup")
    @is_admin()
    async def verify_setup(self, ctx: commands.Context, role: discord.Role, channel: Optional[discord.TextChannel] = None):
        target_chan = channel or ctx.channel
        await VerificationConfig.update(self.bot.db, ctx.guild.id, enabled=1, role_id=role.id, channel_id=target_chan.id)

        embed = discord.Embed(
            title="🛡️ Server Verification Required",
            description="Welcome! To prevent automated raids and gain access to this server, click the **Verify Here** button below and solve the quick CAPTCHA.",
            color=BOT_COLOR
        )
        embed.set_footer(text="Sentinel Verification Engine")
        view = VerifyButtonView(self.bot)
        await target_chan.send(embed=embed, view=view)
        if target_chan != ctx.channel:
            await ctx.send(f"Verification panel deployed to {target_chan.mention}.")


async def setup(bot):
    await bot.add_cog(Verification(bot))

