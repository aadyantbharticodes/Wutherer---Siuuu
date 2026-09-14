from __future__ import annotations
import random
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR


class RPSView(discord.ui.View):
    def __init__(self, author: discord.Member):
        super().__init__(timeout=30)
        self.author = author

    @discord.ui.button(label="Rock", emoji="🪨", style=discord.ButtonStyle.secondary)
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._play(interaction, "rock")

    @discord.ui.button(label="Paper", emoji="📄", style=discord.ButtonStyle.secondary)
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._play(interaction, "paper")

    @discord.ui.button(label="Scissors", emoji="✂️", style=discord.ButtonStyle.secondary)
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._play(interaction, "scissors")

    async def _play(self, interaction: discord.Interaction, user_choice: str):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("This game isn't yours!", ephemeral=True)

        bot_choice = random.choice(["rock", "paper", "scissors"])
        outcomes = {
            ("rock", "scissors"): True,
            ("paper", "rock"): True,
            ("scissors", "paper"): True,
        }

        if user_choice == bot_choice:
            result = f"🤝 It's a tie! Both chose **{user_choice}**."
            color = BOT_COLOR
        elif outcomes.get((user_choice, bot_choice)):
            result = f"🎉 **You won!** Your **{user_choice}** beats my **{bot_choice}**."
            color = BOT_COLOR_SUCCESS
        else:
            result = f"💥 **I won!** My **{bot_choice}** beats your **{user_choice}**."
            color = BOT_COLOR_ERROR

        embed = discord.Embed(title="Rock Paper Scissors", description=result, color=color)
        self.stop()
        await interaction.response.edit_message(embed=embed, view=None)


class Fun(WuthererCog):

    @commands.command(name="8ball", aliases=["eightball"])
    async def eight_ball(self, ctx: commands.Context, *, question: str):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.",
            "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
            "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
            "Very doubtful."
        ]
        embed = discord.Embed(title="🎱 Magic 8-Ball", color=BOT_COLOR)
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=random.choice(responses), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="roll", aliases=["dice"])
    async def roll_dice(self, ctx: commands.Context, sides: int = 6):
        if sides < 2:
            return await ctx.send("The die must have at least 2 sides.")
        res = random.randint(1, sides)
        await ctx.send(f"🎲 You rolled a **{res}** (1-{sides})!")

    @commands.command(name="flip", aliases=["toss"])
    async def flip_coin(self, ctx: commands.Context):
        res = random.choice(["Heads", "Tails"])
        await ctx.send(f"🪙 The coin landed on **{res}**!")

    @commands.command(name="choose", aliases=["pick"])
    async def choose_option(self, ctx: commands.Context, *choices: str):
        if len(choices) < 2:
            return await ctx.send("Provide at least two choices separated by spaces or quotes.")
        picked = random.choice(choices)
        await ctx.send(f"🤔 I choose: **{picked}**!")

    @commands.command(name="rps")
    async def play_rps(self, ctx: commands.Context):
        view = RPSView(ctx.author)
        embed = discord.Embed(
            title="Rock Paper Scissors",
            description="Choose your move below!",
            color=BOT_COLOR
        )
        await ctx.send(embed=embed, view=view)

    @commands.command(name="rate")
    async def rate_thing(self, ctx: commands.Context, *, item: str):
        score = random.randint(0, 10)
        await ctx.send(f"⭐ I'd rate **{item}** a **{score}/10**!")

    @commands.command(name="trivia")
    async def trivia_question(self, ctx: commands.Context):
        trivia_pool = [
            ("What is the capital of Australia?", "Canberra"),
            ("Which planet is closest to the Sun?", "Mercury"),
            ("What is the chemical symbol for Gold?", "Au"),
            ("In what year did the Apollo 11 moon landing occur?", "1969"),
            ("Who painted the Mona Lisa?", "Leonardo da Vinci"),
            ("What is the largest ocean on Earth?", "Pacific Ocean"),
        ]
        q, a = random.choice(trivia_pool)
        embed = discord.Embed(
            title="🧠 Trivia Challenge",
            description=f"**{q}**\n\n*You have 15 seconds to answer in this channel!*",
            color=BOT_COLOR
        )
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == ctx.channel and not m.author.bot

        try:
            msg = await self.bot.wait_for("message", timeout=15.0, check=check)
            if msg.content.lower().strip() == a.lower():
                await ctx.send(f"🎉 Correct, {msg.author.mention}! The answer was **{a}**.")
            else:
                await ctx.send(f"❌ Incorrect! The answer was **{a}**.")
        except Exception:
            await ctx.send(f"⏰ Time's up! The answer was **{a}**.")


async def setup(bot):
    await bot.add_cog(Fun(bot))

