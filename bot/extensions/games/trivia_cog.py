from __future__ import annotations
import random
import discord
from discord.ext import commands
from games.trivia import TRIVIA_BANK, TriviaView


class TriviaCog(commands.Cog, name="Trivia"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="trivia", description="Answer a trivia challenge across Science, Tech, Gaming, History & Geography")
    @commands.describe(category="Optional category filter")
    async def trivia(self, ctx: commands.Context, category: str = None):
        bank = TRIVIA_BANK
        if category:
            filtered = [q for q in bank if q.category.lower() == category.lower()]
            if filtered:
                bank = filtered

        question = random.choice(bank)
        view = TriviaView(ctx.author.id, question, timeout=25.0)
        embed = view.get_initial_embed()
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(TriviaCog(bot))
