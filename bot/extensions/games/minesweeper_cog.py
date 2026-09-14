from __future__ import annotations
import discord
from discord.ext import commands
from games.minesweeper import MinesweeperView


class MinesweeperCog(commands.Cog, name="Minesweeper"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="minesweeper", description="Start an interactive Discord Minesweeper game")
    @commands.describe(difficulty="Difficulty level: easy, medium, hard")
    async def minesweeper(self, ctx: commands.Context, difficulty: str = "easy"):
        diff = difficulty.lower()
        if diff == "hard":
            size, bombs = 5, 6
        elif diff == "medium":
            size, bombs = 5, 4
        else:
            size, bombs = 4, 3

        view = MinesweeperView(ctx.author.id, size=size, bombs=bombs)
        embed = view.get_embed()
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(MinesweeperCog(bot))
