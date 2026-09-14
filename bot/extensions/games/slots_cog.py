from __future__ import annotations
import asyncio
import discord
from discord.ext import commands
from games.slots import SlotMachine
from database.models.economy import EconomyModel


class SlotsCog(commands.Cog, name="Slots"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="slots", aliases=["slot", "spin"], description="Spin the Casino Slot Machine with your chips")
    @commands.describe(bet="Amount of chips to wager (minimum 10)")
    async def slots(self, ctx: commands.Context, bet: int = 50):
        if bet < 10:
            await ctx.send("❌ Minimum bet for Slots is **10** chips.")
            return

        econ = await EconomyModel.get(self.bot.db, ctx.guild.id, ctx.author.id)
        balance = econ.get("wallet", 0)
        if balance < bet:
            await ctx.send(f"❌ You do not have enough chips! Your current wallet balance is **{balance:,}** chips.")
            return

        await EconomyModel.update_balance(self.bot.db, ctx.guild.id, ctx.author.id, wallet=-bet)

        spinning_embed = discord.Embed(
            title="🎰 Casino Slots — Spinning...",
            description="```\n[ 🔄 | 🔄 | 🔄 ]\n```\n*Reels are spinning...*",
            color=0xFEE75C
        )
        msg = await ctx.send(embed=spinning_embed)
        await asyncio.sleep(1.2)

        result, payout = SlotMachine.spin(bet)

        if payout > 0:
            await EconomyModel.update_balance(self.bot.db, ctx.guild.id, ctx.author.id, wallet=payout)

        reels_str = f"[ {' | '.join(result.reels)} ]"
        net_profit = payout - bet

        if result.is_jackpot:
            title = "🚨 MEGA JACKPOT WINNER! 🚨"
            color = 0xFFD700
        elif payout > 0:
            title = "🎉 Casino Slots — Winner!"
            color = 0x57F287
        else:
            title = "🎰 Casino Slots — Loss"
            color = 0xED4245

        embed = discord.Embed(title=title, color=color)
        embed.description = f"```\n{reels_str}\n```\n**{result.description}**\n\n"
        if payout > 0:
            embed.description += f"💰 **Payout:** +{payout:,} chips *(Net Profit: +{net_profit:,})*"
        else:
            embed.description += f"💸 **Loss:** -{bet:,} chips"

        embed.set_footer(text=f"Wager: {bet} chips • Sentinel Casino")
        await msg.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(SlotsCog(bot))
