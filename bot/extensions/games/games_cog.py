from __future__ import annotations

import discord
from discord.ext import commands

from games.battleship import BattleShip
from games.chess_game import Chess


class GamesCog(commands.Cog, name="Games"):
    """Interactive multi-player Discord games."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="battleship",
        aliases=["bs"],
        description="Challenge another player to a game of Battleship (played in DMs)",
    )
    @commands.describe(opponent="The player you want to challenge")
    async def battleship(self, ctx: commands.Context, opponent: discord.Member):
        if opponent.bot:
            return await ctx.send("❌ You cannot challenge a bot to Battleship.")
        if opponent == ctx.author:
            return await ctx.send("❌ You cannot challenge yourself.")

        try:
            game = BattleShip(ctx.author, opponent)
            await game.start(ctx)
        except discord.Forbidden:
            await ctx.send("❌ Could not send DMs. Please ensure both players have DMs enabled for this server!")
        except Exception as exc:
            await ctx.send(f"❌ Failed to start Battleship: {exc}")

    @commands.hybrid_command(
        name="chess",
        description="Challenge another player to a game of Chess",
    )
    @commands.describe(opponent="The player you want to challenge")
    async def chess(self, ctx: commands.Context, opponent: discord.Member):
        if opponent.bot:
            return await ctx.send("❌ You cannot challenge a bot to Chess.")
        if opponent == ctx.author:
            return await ctx.send("❌ You cannot challenge yourself.")

        try:
            await ctx.send(f"♟️ **Chess match started!** {ctx.author.mention} (White) vs {opponent.mention} (Black).\nType UCI moves in chat (e.g. `e2e4`, `e7e5`).")
            game = Chess(white=ctx.author, black=opponent)
            await game.start(ctx)
        except Exception as exc:
            await ctx.send(f"❌ Failed to start Chess: {exc}")


async def setup(bot: commands.Bot):
    await bot.add_cog(GamesCog(bot))
