from __future__ import annotations
import discord
from discord.ext import commands
from games.blackjack import BlackjackView
from database.models.economy import EconomyModel


class BlackjackCog(commands.Cog, name="Casino"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="blackjack", aliases=["bj", "21"], description="Play Casino Blackjack with your economy wallet chips")
    @commands.describe(bet="Amount of chips to wager (minimum 10)")
    async def blackjack(self, ctx: commands.Context, bet: int = 50):
        if bet < 10:
            await ctx.send("❌ Minimum bet for Blackjack is **10** chips.")
            return

        econ = await EconomyModel.get(self.bot.db, ctx.guild.id, ctx.author.id)
        balance = econ.get("wallet", 0)
        if balance < bet:
            await ctx.send(f"❌ You do not have enough chips! Your current wallet balance is **{balance:,}** chips.")
            return

        await EconomyModel.update_balance(self.bot.db, ctx.guild.id, ctx.author.id, wallet=-bet)

        async def on_game_finish(game):
            net_change = 0
            if game.status == "blackjack":
                net_change = int(game.bet * 2.5)
            elif game.status in ("win", "dealer_bust"):
                net_change = game.bet * 2
            elif game.status == "push":
                net_change = game.bet
            elif game.status == "surrender":
                net_change = game.bet

            if net_change > 0:
                await EconomyModel.update_balance(self.bot.db, ctx.guild.id, ctx.author.id, wallet=net_change)

        view = BlackjackView(ctx.author.id, bet=bet, on_finish=on_game_finish)
        embed = view.get_embed()
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(BlackjackCog(bot))
