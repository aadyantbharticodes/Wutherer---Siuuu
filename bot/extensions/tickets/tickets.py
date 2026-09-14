from __future__ import annotations
import asyncio
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_admin, is_mod
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR, BOT_COLOR_WARNING
from database.models.tickets import TicketConfig, TicketManager


class TicketControlView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red, custom_id="ticket_close_btn")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await TicketManager.close(self.bot.db, interaction.channel.id)
        await asyncio.sleep(5)
        try:
            await interaction.channel.delete(reason="Ticket Closed")
        except discord.HTTPException:
            pass

    @discord.ui.button(label="🙋 Claim Ticket", style=discord.ButtonStyle.secondary, custom_id="ticket_claim_btn")
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await TicketManager.claim(self.bot.db, interaction.channel.id, interaction.user.id)
        embed = discord.Embed(
            description=f"Ticket claimed by {interaction.user.mention}.",
            color=BOT_COLOR_SUCCESS
        )
        await interaction.response.send_message(embed=embed)


class TicketPanelView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="📩 Open Ticket", style=discord.ButtonStyle.primary, custom_id="ticket_open_btn")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        cfg = await TicketConfig.get(self.bot.db, interaction.guild.id)
        open_tickets = await TicketManager.get_open_tickets(self.bot.db, interaction.guild.id, interaction.user.id)
        max_open = cfg.get("max_open", 3)

        if len(open_tickets) >= max_open:
            return await interaction.response.send_message(
                f"You already have {len(open_tickets)} open ticket(s). Please close them before opening a new one.",
                ephemeral=True
            )

        category = interaction.guild.get_channel(cfg.get("category_id")) if cfg.get("category_id") else None
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        if cfg.get("support_role_id"):
            supp_role = interaction.guild.get_role(cfg["support_role_id"])
            if supp_role:
                overwrites[supp_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        chan_name = f"ticket-{interaction.user.name[:12]}-{len(open_tickets)+1}"
        channel = await interaction.guild.create_text_channel(
            name=chan_name,
            category=category,
            overwrites=overwrites,
            reason=f"Ticket opened by {interaction.user}"
        )

        await TicketManager.create(self.bot.db, interaction.guild.id, channel.id, interaction.user.id)

        embed = discord.Embed(
            title=f"Support Ticket #{channel.name}",
            description=(
                f"Hello {interaction.user.mention}!\n\n"
                f"{cfg.get('greeting', 'A staff member will assist you shortly.')}\n"
                f"Please explain your inquiry in detail."
            ),
            color=BOT_COLOR
        )
        ctrl_view = TicketControlView(self.bot)
        await channel.send(content=f"{interaction.user.mention}", embed=embed, view=ctrl_view)
        await interaction.response.send_message(f"Ticket opened: {channel.mention}", ephemeral=True)


class Tickets(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)

        self.bot.add_view(TicketPanelView(self.bot))
        self.bot.add_view(TicketControlView(self.bot))

    @commands.group(name="ticket", invoke_without_command=True)
    async def ticket_group(self, ctx: commands.Context):
        await ctx.send_help(ctx.command)

    @ticket_group.command(name="setup")
    @is_admin()
    async def ticket_setup(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        target_chan = channel or ctx.channel
        embed = discord.Embed(
            title="🎫 Support Tickets",
            description="Need assistance? Click the button below to create a private support ticket with staff.",
            color=BOT_COLOR
        )
        embed.set_footer(text="Sentinel Support System")
        view = TicketPanelView(self.bot)
        msg = await target_chan.send(embed=embed, view=view)
        await TicketConfig.update(
            self.bot.db, ctx.guild.id, enabled=1, panel_channel_id=target_chan.id, panel_message_id=msg.id
        )
        if target_chan != ctx.channel:
            await ctx.send(f"Ticket panel deployed in {target_chan.mention}.")

    @ticket_group.command(name="close")
    async def close_ticket(self, ctx: commands.Context):
        ticket = await TicketManager.get_by_channel(self.bot.db, ctx.channel.id)
        if not ticket:
            return await ctx.send("This channel is not an active ticket.")
        await ctx.send("Closing ticket in 5 seconds...")
        await TicketManager.close(self.bot.db, ctx.channel.id)
        await asyncio.sleep(5)
        try:
            await ctx.channel.delete(reason=f"Closed by {ctx.author}")
        except discord.HTTPException:
            pass


async def setup(bot):
    await bot.add_cog(Tickets(bot))

