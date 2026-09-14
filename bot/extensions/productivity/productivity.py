from __future__ import annotations
import asyncio
import datetime
import math
import re
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR
from services.scheduler import scheduler


def parse_duration(time_str: str) -> Optional[int]:
    match = re.match(r"^(\d+)([smhd])$", time_str.lower())
    if not match:
        return None
    val, unit = int(match.group(1)), match.group(2)
    mult = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return val * mult[unit]


class Productivity(WuthererCog):

    @commands.command(name="remindme", aliases=["remind", "reminder"])
    async def create_reminder(self, ctx: commands.Context, duration: str, *, reminder: str):
        seconds = parse_duration(duration)
        if not seconds:
            return await ctx.send("Please provide a valid time (e.g. `10m`, `2h`, `1d`).")

        due_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
        embed = discord.Embed(
            description=f"⏰ I'll remind you <t:{int(due_time.timestamp())}:R> about:\n> {reminder}",
            color=BOT_COLOR_SUCCESS
        )
        await ctx.send(embed=embed)

        async def send_reminder():
            try:
                remind_embed = discord.Embed(
                    title="⏰ Reminder!",
                    description=f"You asked to be reminded about:\n\n> {reminder}",
                    color=BOT_COLOR
                )
                await ctx.author.send(embed=remind_embed)
            except discord.HTTPException:
                try:
                    await ctx.send(f"{ctx.author.mention}", embed=remind_embed)
                except discord.HTTPException:
                    pass

        task_id = f"reminder_{ctx.author.id}_{int(due_time.timestamp())}"
        scheduler.schedule(task_id, float(seconds), send_reminder)

    @commands.command(name="timer")
    async def countdown_timer(self, ctx: commands.Context, duration: str):
        seconds = parse_duration(duration)
        if not seconds or seconds > 3600:
            return await ctx.send("Please specify a time between 1s and 1h.")

        await ctx.send(f"⏳ Timer started for **{duration}**.")
        await asyncio.sleep(seconds)
        await ctx.send(f"🔔 {ctx.author.mention}, your **{duration}** timer is up!")

    @commands.command(name="calc", aliases=["calculate", "math"])
    async def calculate_math(self, ctx: commands.Context, *, expression: str):
        clean_expr = expression.replace("^", "**")
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in clean_expr):
            return await ctx.send("Expression contains forbidden characters.")

        try:

            res = eval(clean_expr, {"__builtins__": None}, {})
            embed = discord.Embed(title="🧮 Calculator", color=BOT_COLOR)
            embed.add_field(name="Input", value=f"`{expression}`", inline=False)
            embed.add_field(name="Result", value=f"`{res}`", inline=False)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send("Invalid mathematical expression.")

    @commands.command(name="convert")
    async def convert_units(self, ctx: commands.Context, value: float, from_unit: str, to_unit: str):
        f = from_unit.lower()
        t = to_unit.lower()


        if f in ("c", "celsius") and t in ("f", "fahrenheit"):
            res = (value * 9/5) + 32
            return await ctx.send(f"🌡️ `{value}°C` = `{res:.2f}°F`")
        if f in ("f", "fahrenheit") and t in ("c", "celsius"):
            res = (value - 32) * 5/9
            return await ctx.send(f"🌡️ `{value}°F` = `{res:.2f}°C`")


        if f in ("km", "kilometers") and t in ("mi", "miles"):
            res = value * 0.621371
            return await ctx.send(f"📏 `{value} km` = `{res:.2f} mi`")
        if f in ("mi", "miles") and t in ("km", "kilometers"):
            res = value * 1.60934
            return await ctx.send(f"📏 `{value} mi` = `{res:.2f} km`")


        if f in ("kg", "kilograms") and t in ("lb", "lbs", "pounds"):
            res = value * 2.20462
            return await ctx.send(f"⚖️ `{value} kg` = `{res:.2f} lbs`")
        if f in ("lb", "lbs", "pounds") and t in ("kg", "kilograms"):
            res = value / 2.20462
            return await ctx.send(f"⚖️ `{value} lbs` = `{res:.2f} kg`")

        await ctx.send("Conversion pair not supported. (Supported: C/F, km/mi, kg/lb)")


async def setup(bot):
    await bot.add_cog(Productivity(bot))

