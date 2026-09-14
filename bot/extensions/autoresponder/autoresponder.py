from __future__ import annotations

import re
import time
from typing import TYPE_CHECKING, Dict, Optional

import discord
from discord.ext import commands

from bot.core.cog import WuthererCog
from bot.core.context import WuthererContext
from bot.core.checks import is_admin
from bot.database.models.autoresponder import AutoResponderModel, AutoResponseTrigger

if TYPE_CHECKING:
    from bot.core.bot import WuthererBot


class AutoResponder(WuthererCog, name="AutoResponder"):

    def __init__(self, bot: WuthererBot) -> None:
        super().__init__(bot)

        self._cooldowns: Dict[tuple[int, int], float] = {}

    @WuthererCog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not message.guild:
            return

        if not self.bot.db_pool:
            return


        async with self.bot.db_pool.acquire() as db:
            dao = AutoResponderModel(db)
            triggers = await dao.list_triggers(message.guild.id)

        if not triggers:
            return

        content_lower = message.content.lower().strip()
        raw_content = message.content.strip()
        now = time.time()

        for trigger in triggers:
            if not trigger.enabled:
                continue


            cd_key = (message.guild.id, trigger.trigger_id)
            last_used = self._cooldowns.get(cd_key, 0.0)
            if now - last_used < trigger.cooldown_seconds:
                continue


            matched = False
            if trigger.match_mode == "exact":
                matched = (content_lower == trigger.trigger_text.lower())
            elif trigger.match_mode == "wildcard":
                matched = (trigger.trigger_text.lower() in content_lower)
            elif trigger.match_mode == "regex":
                try:
                    matched = bool(re.search(trigger.trigger_text, raw_content, re.IGNORECASE))
                except re.error:
                    pass

            if matched:
                self._cooldowns[cd_key] = now
                await self._execute_response(message, trigger)

                async with self.bot.db_pool.acquire() as db:
                    dao = AutoResponderModel(db)
                    await dao.increment_uses(trigger.trigger_id)
                break

    async def _execute_response(self, message: discord.Message, trigger: AutoResponseTrigger) -> None:

        text = trigger.response_text
        text = text.replace("{user}", message.author.mention)
        text = text.replace("{username}", message.author.name)
        text = text.replace("{server}", message.guild.name)
        text = text.replace("{channel}", message.channel.mention)

        if trigger.delete_trigger:
            try:
                await message.delete()
            except discord.HTTPException:
                pass

        if trigger.is_embed:
            color = trigger.embed_color if trigger.embed_color else self.bot.embed.COLOR_PRIMARY
            embed = self.bot.embed.create(
                description=text,
                color=color,
            )
            embed.set_footer(text="Sentinel Auto-Responder")
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(text)

    @commands.group(name="autoresponder", aliases=["ar", "triggers"], invoke_without_command=True)
    @is_admin()
    async def ar_group(self, ctx: WuthererContext) -> None:
        await ctx.send_help(ctx.command)

    @ar_group.command(name="add", aliases=["create"])
    @is_admin()
    async def ar_add(self, ctx: WuthererContext, *, raw_args: str) -> None:
        is_embed = "--embed" in raw_args
        raw_args = raw_args.replace("--embed", "")

        match_mode = "exact"
        if "--mode=wildcard" in raw_args:
            match_mode = "wildcard"
            raw_args = raw_args.replace("--mode=wildcard", "")
        elif "--mode=regex" in raw_args:
            match_mode = "regex"
            raw_args = raw_args.replace("--mode=regex", "")

        if "|" not in raw_args:
            await ctx.send_error("Please separate the trigger keyword and response using `|`.\nExample: `s!ar add hello | Welcome to our server!`")
            return

        parts = raw_args.split("|", 1)
        trigger_text = parts[0].strip()
        response_text = parts[1].strip()

        if not trigger_text or not response_text:
            await ctx.send_error("Trigger and response text cannot be empty.")
            return

        if match_mode == "regex":
            try:
                re.compile(trigger_text)
            except re.error as e:
                await ctx.send_error(f"Invalid regex syntax: `{e}`")
                return

        async with self.bot.db_pool.acquire() as db:
            dao = AutoResponderModel(db)
            trigger_id = await dao.add_trigger(
                guild_id=ctx.guild.id,
                trigger_text=trigger_text,
                response_text=response_text,
                match_mode=match_mode,
                is_embed=is_embed,
                created_by=ctx.author.id,
            )

        embed = self.bot.embed.create(
            title="⚡ Trigger Activated",
            description=f"Auto-responder created successfully with ID **`#{trigger_id}`**.",
            color=self.bot.embed.COLOR_SUCCESS,
        )
        embed.add_field(name="Trigger Keyword", value=f"`{trigger_text}`", inline=True)
        embed.add_field(name="Mode", value=f"`{match_mode}`", inline=True)
        embed.add_field(name="Embed Formatted", value=f"`{'Yes' if is_embed else 'No'}`", inline=True)
        embed.add_field(name="Response", value=f"{response_text[:300]}", inline=False)

        await ctx.send(embed=embed)

    @ar_group.command(name="list", aliases=["show"])
    @is_admin()
    async def ar_list(self, ctx: WuthererContext) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = AutoResponderModel(db)
            triggers = await dao.list_triggers(ctx.guild.id)

        if not triggers:
            await ctx.send_warn("No auto-responders configured for this server. Use `s!ar add` to create one.")
            return

        embed = self.bot.embed.create(
            title=f"📋 Auto-Responders — {ctx.guild.name}",
            description=f"Total Triggers: `{len(triggers)}`",
        )

        for t in triggers[:15]:
            status = "🟢 Active" if t.enabled else "🔴 Disabled"
            desc = (
                f"• **Status:** {status} | **Mode:** `{t.match_mode}`\n"
                f"• **Uses:** `{t.uses_count}` | **Embed:** `{'Yes' if t.is_embed else 'No'}`\n"
                f"• **Response Preview:** {t.response_text[:80]}...\n"
            )
            embed.add_field(name=f"ID `#{t.trigger_id}`: \"{t.trigger_text}\"", value=desc, inline=False)

        await ctx.send(embed=embed)

    @ar_group.command(name="delete", aliases=["remove"])
    @is_admin()
    async def ar_delete(self, ctx: WuthererContext, trigger_id: int) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = AutoResponderModel(db)
            deleted = await dao.delete_trigger(trigger_id, ctx.guild.id)

        if deleted:
            await ctx.send_success(f"Trigger `#{trigger_id}` has been deleted.")
        else:
            await ctx.send_error(f"Trigger `#{trigger_id}` was not found.")

    @ar_group.command(name="toggle")
    @is_admin()
    async def ar_toggle(self, ctx: WuthererContext, trigger_id: int) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = AutoResponderModel(db)
            trigger = await dao.get_trigger(trigger_id, ctx.guild.id)
            if not trigger:
                await ctx.send_error(f"Trigger `#{trigger_id}` was not found.")
                return

            new_state = not trigger.enabled
            await dao.set_enabled(trigger_id, ctx.guild.id, new_state)

        state_str = "Enabled" if new_state else "Disabled"
        await ctx.send_success(f"Trigger `#{trigger_id}` is now **{state_str}**.")


async def setup(bot: WuthererBot) -> None:
    await bot.add_cog(AutoResponder(bot))

