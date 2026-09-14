from __future__ import annotations
import discord
from typing import Optional

from config import BOT_COLOR


class Paginator(discord.ui.View):
    def __init__(self, ctx, entries: list[str], per_page: int = 10,
                 title: str = None, timeout: float = 120.0):
                     pass
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.entries = entries
        self.per_page = per_page
        self.title = title
        self.page = 0
        self.max_pages = max(1, (len(entries) + per_page - 1) // per_page)
        self.message: Optional[discord.Message] = None

    def get_embed(self) -> discord.Embed:
        start = self.page * self.per_page
        end = start + self.per_page
        description = "\n".join(self.entries[start:end])

        embed = discord.Embed(color=BOT_COLOR, description=description)
        if self.title:
            embed.title = self.title
        embed.set_footer(text=f"Page {self.page + 1}/{self.max_pages} | {len(self.entries)} entries")
        return embed

    async def start(self):
        if not self.entries:
            return await self.ctx.send(embed=discord.Embed(
                color=BOT_COLOR, description="No entries to display."
            ))

        embed = self.get_embed()
        if self.max_pages <= 1:
            return await self.ctx.send(embed=embed)
        self.message = await self.ctx.send(embed=embed, view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "This menu isn't for you.", ephemeral=True
            )
            return False
        return True

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.edit(view=None)
            except discord.HTTPException:
                pass

    async def _update(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="<<", style=discord.ButtonStyle.grey)
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = 0
        await self._update(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = max(0, self.page - 1)
        await self._update(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = min(self.max_pages - 1, self.page + 1)
        await self._update(interaction)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.grey)
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = self.max_pages - 1
        await self._update(interaction)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.message:
            try:
                await self.message.delete()
            except discord.HTTPException:
                pass
        self.stop()


class EmbedPaginator(discord.ui.View):
    def __init__(self, ctx, embeds: list[discord.Embed], timeout: float = 120.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.embeds = embeds
        self.page = 0
        self.message: Optional[discord.Message] = None

    async def start(self):
        if not self.embeds:
            return
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1}/{len(self.embeds)}")
        if len(self.embeds) == 1:
            return await self.ctx.send(embed=self.embeds[0])
        self.message = await self.ctx.send(embed=self.embeds[0], view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "This menu isn't for you.", ephemeral=True
            )
            return False
        return True

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.edit(view=None)
            except discord.HTTPException:
                pass

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = max(0, self.page - 1)
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = min(len(self.embeds) - 1, self.page + 1)
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

