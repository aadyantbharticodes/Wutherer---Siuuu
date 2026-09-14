from __future__ import annotations
from typing import Optional
import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_admin
from config import BOT_COLOR, BOT_COLOR_ERROR, BOT_COLOR_SUCCESS
from services.ai import AIService
from database.models.ai import AIConfigModel


class AI(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.ai = AIService()

    @commands.group(name="ai", invoke_without_command=True)
    async def ai_group(self, ctx: commands.Context, *, prompt: str):
        await self.ai_ask(ctx, prompt=prompt)

    @ai_group.command(name="ask", aliases=["chat", "prompt"])
    async def ai_ask(self, ctx: commands.Context, *, prompt: str):
        async with ctx.typing():
            guild_id = ctx.guild.id if ctx.guild else 0
            cfg = await AIConfigModel.get(self.bot.db, guild_id) if ctx.guild else {}
            persona = cfg.get("persona")


            history = await AIConfigModel.get_history(self.bot.db, guild_id, ctx.author.id, limit=6) if ctx.guild else []
            messages = [{"role": h["role"], "content": h["content"]} for h in history]
            messages.append({"role": "user", "content": prompt})

            resp = await self.ai.chat(messages, system_prompt=persona)
            if not resp:
                return await ctx.send("Sorry, AI service is currently unavailable or API key is not configured.")

            if ctx.guild:
                await AIConfigModel.add_history(self.bot.db, guild_id, ctx.author.id, "user", prompt)
                await AIConfigModel.add_history(self.bot.db, guild_id, ctx.author.id, "assistant", resp)


            if len(resp) > 2000:
                chunks = [resp[i:i + 1950] for i in range(0, len(resp), 1950)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                embed = discord.Embed(description=resp, color=BOT_COLOR)
                embed.set_author(name=f"AI Response for {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
                embed.set_footer(text="Powered by Google Gemini")
                await ctx.send(embed=embed)

    @ai_group.command(name="clear", aliases=["reset", "forget"])
    async def ai_clear(self, ctx: commands.Context):
        guild_id = ctx.guild.id if ctx.guild else 0
        await AIConfigModel.clear_history(self.bot.db, guild_id, ctx.author.id)
        await ctx.send(embed=discord.Embed(
            description="Your conversation history with AI has been cleared.",
            color=BOT_COLOR_SUCCESS
        ))

    @ai_group.command(name="summarize")
    async def ai_summarize(self, ctx: commands.Context, *, text: str):
        async with ctx.typing():
            prompt = f"Summarize the following text clearly and concisely using bullet points:\n\n{text}"
            res = await self.ai.generate(prompt)
            if not res:
                return await ctx.send("Unable to generate summary.")
            embed = discord.Embed(title="Summary", description=res, color=BOT_COLOR)
            await ctx.send(embed=embed)

    @ai_group.command(name="rewrite")
    async def ai_rewrite(self, ctx: commands.Context, style: str, *, text: str):
        async with ctx.typing():
            prompt = f"Rewrite the following text in a {style} tone:\n\n{text}"
            res = await self.ai.generate(prompt)
            if not res:
                return await ctx.send("Unable to rewrite text.")
            embed = discord.Embed(title=f"Rewritten ({style.title()})", description=res, color=BOT_COLOR)
            await ctx.send(embed=embed)

    @ai_group.command(name="translate")
    async def ai_translate(self, ctx: commands.Context, target_language: str, *, text: str):
        async with ctx.typing():
            prompt = f"Translate the following text into {target_language}. Return ONLY the translation:\n\n{text}"
            res = await self.ai.generate(prompt)
            if not res:
                return await ctx.send("Unable to translate.")
            embed = discord.Embed(title=f"Translation ({target_language.title()})", description=res, color=BOT_COLOR)
            await ctx.send(embed=embed)

    @ai_group.command(name="code")
    async def ai_code(self, ctx: commands.Context, language: str, *, question: str):
        async with ctx.typing():
            prompt = (
                f"You are a principal software engineer. Provide clean, well-commented code in {language} "
                f"to answer the following problem:\n{question}"
            )
            res = await self.ai.generate(prompt)
            if not res:
                return await ctx.send("Unable to assist with code.")
            if len(res) > 2000:
                chunks = [res[i:i + 1950] for i in range(0, len(res), 1950)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(res)

    @ai_group.command(name="persona")
    @is_admin()
    async def ai_persona(self, ctx: commands.Context, *, persona: str):
        await AIConfigModel.update(self.bot.db, ctx.guild.id, persona=persona)
        await ctx.send(embed=discord.Embed(
            description=f"AI persona updated to:\n> *{persona}*",
            color=BOT_COLOR_SUCCESS
        ))


async def setup(bot):
    await bot.add_cog(AI(bot))

