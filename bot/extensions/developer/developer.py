from __future__ import annotations
import base64
import hashlib
import json
import re
import time
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_COLOR, BOT_COLOR_ERROR


class Developer(WuthererCog):

    @commands.group(name="dev", aliases=["developer"], invoke_without_command=True)
    async def dev_group(self, ctx: commands.Context):
        await ctx.send_help(ctx.command)

    @dev_group.command(name="json")
    async def format_json(self, ctx: commands.Context, *, raw_json: str):
        raw = raw_json.strip("` ")
        if raw.startswith("json\n"):
            raw = raw[5:]
        try:
            parsed = json.loads(raw)
            formatted = json.dumps(parsed, indent=2)
            if len(formatted) > 1900:
                await ctx.send("Formatted JSON exceeds 2000 characters.")
            else:
                await ctx.send(f"```json\n{formatted}\n```")
        except json.JSONDecodeError as err:
            await ctx.send(embed=discord.Embed(
                title="Invalid JSON",
                description=f"```\n{err}\n```",
                color=BOT_COLOR_ERROR
            ))

    @dev_group.command(name="regex")
    async def test_regex(self, ctx: commands.Context, pattern: str, *, test_string: str):
        try:
            matches = list(re.finditer(pattern, test_string))
            if not matches:
                return await ctx.send("No matches found.")
            results = []
            for i, m in enumerate(matches[:15]):
                results.append(f"Match {i+1}: `{m.group(0)}` (span: {m.span()})")
            embed = discord.Embed(
                title=f"Regex Results: `{pattern}`",
                description="\n".join(results),
                color=BOT_COLOR
            )
            embed.set_footer(text=f"Total matches: {len(matches)}")
            await ctx.send(embed=embed)
        except re.error as err:
            await ctx.send(f"Invalid regex: `{err}`")

    @dev_group.command(name="base64")
    async def b64_tool(self, ctx: commands.Context, mode: str, *, text: str):
        m = mode.lower()
        if m in ("encode", "enc"):
            encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            await ctx.send(f"```\n{encoded}\n```")
        elif m in ("decode", "dec"):
            try:
                decoded = base64.b64decode(text.encode("utf-8")).decode("utf-8")
                await ctx.send(f"```\n{decoded}\n```")
            except Exception:
                await ctx.send("Failed to decode base64 string.")
        else:
            await ctx.send("Mode must be `encode` or `decode`.")

    @dev_group.command(name="hash")
    async def generate_hash(self, ctx: commands.Context, algorithm: str, *, text: str):
        algo = algorithm.lower()
        if algo not in hashlib.algorithms_available:
            return await ctx.send(f"Unsupported algorithm. Available: md5, sha1, sha256, sha512")
        h = hashlib.new(algo, text.encode("utf-8")).hexdigest()
        embed = discord.Embed(title=f"{algo.upper()} Hash", description=f"`{h}`", color=BOT_COLOR)
        await ctx.send(embed=embed)

    @dev_group.command(name="timestamp", aliases=["ts"])
    async def timestamp_helper(self, ctx: commands.Context, unix_seconds: Optional[int] = None):
        t = unix_seconds or int(time.time())
        formats = [
            ("Default (<t:t>)", f"<t:{t}>", f"`<t:{t}>`"),
            ("Short Time (<t:t:t>)", f"<t:{t}:t>", f"`<t:{t}:t>`"),
            ("Long Time (<t:t:T>)", f"<t:{t}:T>", f"`<t:{t}:T>`"),
            ("Short Date (<t:t:d>)", f"<t:{t}:d>", f"`<t:{t}:d>`"),
            ("Long Date (<t:t:D>)", f"<t:{t}:D>", f"`<t:{t}:D>`"),
            ("Short Date/Time (<t:t:f>)", f"<t:{t}:f>", f"`<t:{t}:f>`"),
            ("Long Date/Time (<t:t:F>)", f"<t:{t}:F>", f"`<t:{t}:F>`"),
            ("Relative Time (<t:t:R>)", f"<t:{t}:R>", f"`<t:{t}:R>`"),
        ]
        embed = discord.Embed(title=f"Discord Timestamps for `{t}`", color=BOT_COLOR)
        for name, preview, code in formats:
            embed.add_field(name=name, value=f"{preview} • {code}", inline=False)
        await ctx.send(embed=embed)

    @dev_group.command(name="color", aliases=["hex"])
    async def color_preview(self, ctx: commands.Context, hex_code: str):
        clean_hex = hex_code.strip("#")
        try:
            val = int(clean_hex, 16)
        except ValueError:
            return await ctx.send("Invalid hex color code.")
        r = (val >> 16) & 255
        g = (val >> 8) & 255
        b = val & 255
        embed = discord.Embed(
            title=f"Color Preview: #{clean_hex.upper()}",
            description=f"**RGB:** `{r}, {g}, {b}`\n**Decimal:** `{val}`",
            color=val
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Developer(bot))

