from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import discord
from discord.ext import commands

from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR, BOT_COLOR_WARNING

if TYPE_CHECKING:
    from core.bot import WuthererBot


class Context(commands.Context):
    bot: WuthererBot

    async def success(self, message: str, **kwargs) -> discord.Message:
        embed = discord.Embed(color=BOT_COLOR_SUCCESS, description=message)
        return await self.send(embed=embed, **kwargs)

    async def error(self, message: str, **kwargs) -> discord.Message:
        embed = discord.Embed(color=BOT_COLOR_ERROR, description=message)
        return await self.send(embed=embed, **kwargs)

    async def warn(self, message: str, **kwargs) -> discord.Message:
        embed = discord.Embed(color=BOT_COLOR_WARNING, description=message)
        return await self.send(embed=embed, **kwargs)

    async def info(self, message: str, **kwargs) -> discord.Message:
        embed = discord.Embed(color=BOT_COLOR, description=message)
        return await self.send(embed=embed, **kwargs)

    async def confirm(self, message: str, timeout: float = 30.0) -> bool:
        embed = discord.Embed(color=BOT_COLOR_WARNING, description=message)
        view = ConfirmView(self.author, timeout=timeout)
        msg = await self.send(embed=embed, view=view)
        await view.wait()
        try:
            await msg.delete()
        except discord.HTTPException:
            pass
        return view.value

    async def paginate(self, entries: list[str], per_page: int = 10, title: str = None):
        from services.pagination import Paginator
        paginator = Paginator(self, entries, per_page=per_page, title=title)
        await paginator.start()


class ConfirmView(discord.ui.View):
    value: Optional[bool] = None

    def __init__(self, author: discord.Member, timeout: float = 30.0):
        super().__init__(timeout=timeout)
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "This confirmation isn't for you.", ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.defer()
        self.stop()

