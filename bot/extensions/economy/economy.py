from __future__ import annotations
import datetime
import random
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR, BOT_COLOR_WARNING
from database.models.economy import EconomyModel


class Economy(WuthererCog):

    @commands.command(name="balance", aliases=["bal"])
    async def view_balance(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        target = member or ctx.author
        acc = await EconomyModel.get_account(self.bot.db, ctx.guild.id, target.id)
        embed = discord.Embed(
            title=f"💰 Balance — {target.display_name}",
            color=BOT_COLOR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Wallet", value=f"🪙 **{acc['wallet']:,}** credits", inline=True)
        embed.add_field(name="Bank", value=f"🏦 **{acc['bank']:,}** credits", inline=True)
        embed.add_field(name="Total Net Worth", value=f"✨ **{(acc['wallet'] + acc['bank']):,}** credits", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="daily")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def claim_daily(self, ctx: commands.Context):
        amount = 250
        await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, amount)
        await EconomyModel.set_daily(self.bot.db, ctx.guild.id, ctx.author.id)
        embed = discord.Embed(
            description=f"🎉 You claimed your daily reward of 🪙 **{amount:,}** credits!",
            color=BOT_COLOR_SUCCESS
        )
        await ctx.send(embed=embed)

    @commands.command(name="work")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def do_work(self, ctx: commands.Context):
        jobs = [
            ("software engineer", 120),
            ("Discord moderator", 85),
            ("data scientist", 150),
            ("graphic designer", 100),
            ("server architect", 140),
            ("coffee barista", 75),
        ]
        job, pay = random.choice(jobs)
        wage = pay + random.randint(-15, 25)
        await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, wage)
        await EconomyModel.set_work(self.bot.db, ctx.guild.id, ctx.author.id)
        await ctx.send(embed=discord.Embed(
            description=f"💼 You worked as a **{job}** and earned 🪙 **{wage:,}** credits!",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="deposit", aliases=["dep"])
    async def deposit_funds(self, ctx: commands.Context, amount: str):
        acc = await EconomyModel.get_account(self.bot.db, ctx.guild.id, ctx.author.id)
        val = acc["wallet"] if amount.lower() in ("all", "max") else int(amount)
        if val <= 0 or val > acc["wallet"]:
            return await ctx.send("Invalid deposit amount.")

        await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, -val)
        await EconomyModel.modify_bank(self.bot.db, ctx.guild.id, ctx.author.id, val)
        await ctx.send(embed=discord.Embed(
            description=f"🏦 Deposited 🪙 **{val:,}** credits into your bank.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="withdraw", aliases=["with"])
    async def withdraw_funds(self, ctx: commands.Context, amount: str):
        acc = await EconomyModel.get_account(self.bot.db, ctx.guild.id, ctx.author.id)
        val = acc["bank"] if amount.lower() in ("all", "max") else int(amount)
        if val <= 0 or val > acc["bank"]:
            return await ctx.send("Invalid withdrawal amount.")

        await EconomyModel.modify_bank(self.bot.db, ctx.guild.id, ctx.author.id, -val)
        await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, val)
        await ctx.send(embed=discord.Embed(
            description=f"🪙 Withdrew **{val:,}** credits from your bank.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="pay", aliases=["transfer"])
    async def transfer_money(self, ctx: commands.Context, recipient: discord.Member, amount: int):
        if recipient.id == ctx.author.id or recipient.bot:
            return await ctx.send("Cannot transfer credits to this recipient.")
        if amount <= 0:
            return await ctx.send("Transfer amount must be positive.")

        sender_acc = await EconomyModel.get_account(self.bot.db, ctx.guild.id, ctx.author.id)
        if sender_acc["wallet"] < amount:
            return await ctx.send("You do not have enough credits in your wallet.")

        await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, -amount)
        await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, recipient.id, amount)
        await ctx.send(embed=discord.Embed(
            description=f"💸 Successfully sent 🪙 **{amount:,}** credits to {recipient.mention}!",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="coinflip", aliases=["cf"])
    async def coin_flip_gamble(self, ctx: commands.Context, bet: int, choice: str):
        c = choice.lower()
        if c not in ("heads", "tails", "h", "t"):
            return await ctx.send("Choose `heads` or `tails`.")
        chosen = "heads" if c in ("heads", "h") else "tails"

        acc = await EconomyModel.get_account(self.bot.db, ctx.guild.id, ctx.author.id)
        if bet <= 0 or bet > acc["wallet"]:
            return await ctx.send("Invalid bet amount or insufficient funds.")

        outcome = random.choice(["heads", "tails"])
        won = (outcome == chosen)
        change = bet if won else -bet
        await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, change)

        embed = discord.Embed(
            title=f"🪙 Coinflip: {outcome.upper()}",
            description=(
                f"You guessed **{chosen}**.\n"
                f"{'🎉 **You won** 🪙 **' + str(bet) + '** credits!' if won else '💥 **You lost** 🪙 **' + str(bet) + '** credits.'}"
            ),
            color=BOT_COLOR_SUCCESS if won else BOT_COLOR_ERROR
        )
        await ctx.send(embed=embed)

    @commands.command(name="slots")
    async def slot_machine(self, ctx: commands.Context, bet: int):
        acc = await EconomyModel.get_account(self.bot.db, ctx.guild.id, ctx.author.id)
        if bet <= 0 or bet > acc["wallet"]:
            return await ctx.send("Invalid bet amount.")

        emojis = ["🍒", "🍋", "🍇", "🔔", "💎", "7️⃣"]
        reel1 = random.choice(emojis)
        reel2 = random.choice(emojis)
        reel3 = random.choice(emojis)

        if reel1 == reel2 == reel3:
            multiplier = 5 if reel1 == "💎" else 3
            payout = bet * multiplier
            await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, payout)
            status = f"JACKPOT! You won 🪙 **{payout:,}** credits!"
            color = BOT_COLOR_SUCCESS
        elif reel1 == reel2 or reel2 == reel3 or reel1 == reel3:
            payout = int(bet * 1.5)
            await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, payout - bet)
            status = f"Nice! Two matching. You won 🪙 **{payout:,}** credits!"
            color = BOT_COLOR_SUCCESS
        else:
            await EconomyModel.modify_wallet(self.bot.db, ctx.guild.id, ctx.author.id, -bet)
            status = f"No match. You lost 🪙 **{bet:,}** credits."
            color = BOT_COLOR_ERROR

        embed = discord.Embed(
            title="🎰 Slot Machine",
            description=f"| {reel1} | {reel2} | {reel3} |\n\n{status}",
            color=color
        )
        await ctx.send(embed=embed)

    @commands.command(name="economyleaderboard", aliases=["rich", "baltop"])
    async def economy_lb(self, ctx: commands.Context):
        top = await EconomyModel.get_leaderboard(self.bot.db, ctx.guild.id, limit=10)
        lines = []
        for i, row in enumerate(top):
            member = ctx.guild.get_member(row["user_id"])
            name = member.display_name if member else f"User {row['user_id']}"
            lines.append(f"**{i+1}.** {name} — 🪙 **{row['total']:,}** credits")

        embed = discord.Embed(
            title=f"🏆 Wealth Leaderboard — {ctx.guild.name}",
            description="\n".join(lines) if lines else "No economy data available.",
            color=BOT_COLOR
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))

