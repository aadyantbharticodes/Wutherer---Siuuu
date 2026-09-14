from __future__ import annotations
import discord
from discord.ext import commands
from games.uno import UnoGame, UnoView


class UnoCog(commands.Cog, name="Uno"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="uno", description="Start an interactive 2-player Uno match")
    @commands.describe(opponent="The player you wish to challenge")
    async def uno(self, ctx: commands.Context, opponent: discord.Member):
        if opponent.id == ctx.author.id:
            await ctx.send("❌ You cannot play Uno against yourself! Challenge a friend.")
            return

        if opponent.bot:
            await ctx.send("❌ Bots cannot play Uno.")
            return

        game = UnoGame([ctx.author, opponent])
        view = UnoView(game)
        embed = view.get_embed(status_note=f"Game started! {ctx.author.name} vs {opponent.name}")
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(UnoCog(bot))
