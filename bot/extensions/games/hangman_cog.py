from __future__ import annotations
import asyncio
import discord
from discord.ext import commands
from games.hangman import HangmanView, WORD_CATEGORIES


class HangmanCog(commands.Cog, name="Hangman"):
    def __init__(self, bot):
        self.bot = bot
        self.active_games: dict[int, HangmanView] = {}

    @commands.hybrid_command(name="hangman", description="Start an interactive game of Hangman")
    @commands.describe(category="Optional category: Gaming, Programming, Science, Countries, Anime")
    async def hangman(self, ctx: commands.Context, category: str = None):
        if ctx.channel.id in self.active_games:
            await ctx.send("❌ There is already an active Hangman session in this channel!")
            return

        cat = None
        if category:
            for k in WORD_CATEGORIES:
                if k.lower() == category.lower():
                    cat = k
                    break

        view = HangmanView(ctx.author.id, category=cat)
        self.active_games[ctx.channel.id] = view
        embed = view.get_embed()
        msg = await ctx.send(embed=embed, view=view)

        def check(m: discord.Message):
            return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id and len(m.content) == 1 and m.content.isalpha()

        while not view.game.game_over:
            try:
                guess_msg = await self.bot.wait_for("message", timeout=60.0, check=check)
                letter = guess_msg.content.upper()
                try:
                    await guess_msg.delete()
                except Exception:
                    pass

                view.game.guess(letter)
                embed = view.get_embed()
                await msg.edit(embed=embed, view=view)
            except asyncio.TimeoutError:
                view.game.game_over = True
                view.game.won = False
                embed = view.get_embed()
                embed.description += "\n\n⏱️ *Game timed out due to inactivity.*"
                await msg.edit(embed=embed, view=view)
                break

        self.active_games.pop(ctx.channel.id, None)


async def setup(bot):
    await bot.add_cog(HangmanCog(bot))
