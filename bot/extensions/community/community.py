from __future__ import annotations
import asyncio
import datetime
import random
import re
from typing import Optional, Union

import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_admin, is_mod
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR, BOT_COLOR_WARNING
from database.models.giveaways import GiveawayModel
from database.models.polls import PollModel
from database.models.starboard import StarboardModel
from database.models.guild import GuildSettings


def parse_time(time_str: str) -> Optional[int]:
    match = re.match(r"^(\d+)([smhd])$", time_str.lower())
    if not match:
        return None
    val, unit = int(match.group(1)), match.group(2)
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return val * multipliers[unit]


class GiveawayView(discord.ui.View):
    def __init__(self, message_id: int, bot):
        super().__init__(timeout=None)
        self.message_id = message_id
        self.bot = bot

    @discord.ui.button(label="🎉 Enter Giveaway", style=discord.ButtonStyle.primary, custom_id="gw_enter")
    async def enter_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        gw = await GiveawayModel.get_by_message(self.bot.db, interaction.message.id)
        if not gw or gw["ended"]:
            return await interaction.response.send_message("This giveaway has ended.", ephemeral=True)

        if gw.get("required_role_id"):
            req_role = interaction.guild.get_role(gw["required_role_id"])
            if req_role and req_role not in interaction.user.roles:
                return await interaction.response.send_message(
                    f"You need the **{req_role.name}** role to enter this giveaway.", ephemeral=True
                )

        added, total = await GiveawayModel.add_entry(self.bot.db, interaction.message.id, interaction.user.id)
        msg = f"🎉 Entered! (Total entries: {total})" if added else f"❌ Left giveaway. (Total entries: {total})"
        await interaction.response.send_message(msg, ephemeral=True)


class Community(WuthererCog):

    @commands.group(name="giveaway", aliases=["g"], invoke_without_command=True)
    @is_mod()
    async def giveaway_group(self, ctx: commands.Context):
        await ctx.send_help(ctx.command)

    @giveaway_group.command(name="start")
    @is_mod()
    async def giveaway_start(self, ctx: commands.Context, duration: str, winners: int, *, prize: str):
        seconds = parse_time(duration)
        if not seconds or seconds < 10:
            return await ctx.send("Please provide a valid duration (e.g. `30s`, `10m`, `2h`, `1d`).")
        if winners < 1:
            return await ctx.send("Winner count must be at least 1.")

        end_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
        embed = discord.Embed(
            title=f"🎁 GIVEAWAY: {prize}",
            description=(
                f"React with 🎉 below to enter!\n\n"
                f"**Winners:** {winners}\n"
                f"**Ends:** <t:{int(end_time.timestamp())}:R>\n"
                f"**Hosted by:** {ctx.author.mention}"
            ),
            color=BOT_COLOR,
            timestamp=end_time
        )
        embed.set_footer(text="Ends at")

        msg = await ctx.send(embed=embed)
        view = GiveawayView(msg.id, self.bot)
        await msg.edit(view=view)

        await GiveawayModel.create(
            self.bot.db, ctx.guild.id, ctx.channel.id, msg.id, ctx.author.id, prize, winners, end_time.isoformat()
        )

    @giveaway_group.command(name="reroll")
    @is_mod()
    async def giveaway_reroll(self, ctx: commands.Context, message_id: int):
        gw = await GiveawayModel.get_by_message(self.bot.db, message_id)
        if not gw:
            return await ctx.send("Giveaway not found.")
        entries = gw["entries"]
        if not entries:
            return await ctx.send("No participants entered this giveaway.")
        winner_id = random.choice(entries)
        winner = ctx.guild.get_member(winner_id) or f"<@{winner_id}>"
        await ctx.send(f"🎉 The new winner for **{gw['prize']}** is {winner}!")

    @commands.command(name="poll")
    async def create_poll(self, ctx: commands.Context, question: str, *options: str):
        if len(options) < 2:
            return await ctx.send("Please provide at least 2 options for the poll.")
        if len(options) > 10:
            return await ctx.send("Maximum of 10 options allowed.")

        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        desc = "\n\n".join(f"{reactions[i]} {opt}" for i, opt in enumerate(options))
        embed = discord.Embed(
            title=f"📊 {question}",
            description=desc,
            color=BOT_COLOR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_footer(text=f"Poll by {ctx.author.display_name}")

        msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await msg.add_reaction(reactions[i])

    @commands.command(name="suggest")
    async def create_suggestion(self, ctx: commands.Context, *, suggestion: str):
        settings = await GuildSettings.get(self.bot.db, ctx.guild.id)
        chan_id = settings.get("suggestion_channel_id")
        channel = ctx.guild.get_channel(chan_id) if chan_id else ctx.channel

        embed = discord.Embed(
            title="💡 New Suggestion",
            description=suggestion,
            color=BOT_COLOR,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text="React to vote")

        msg = await channel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        if channel != ctx.channel:
            await ctx.send(embed=discord.Embed(
                description=f"Suggestion posted in {channel.mention}!",
                color=BOT_COLOR_SUCCESS
            ))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != "⭐" or not payload.guild_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        settings = await GuildSettings.get(self.bot.db, guild.id)
        sb_chan_id = settings.get("starboard_channel_id")
        if not sb_chan_id:
            return
        sb_channel = guild.get_channel(sb_chan_id)
        if not sb_channel:
            return

        source_channel = guild.get_channel(payload.channel_id)
        if not source_channel:
            return
        try:
            message = await source_channel.fetch_message(payload.message_id)
        except (discord.NotFound, discord.HTTPException):
            return

        if message.author.id == payload.user_id:
            return

        reaction = discord.utils.get(message.reactions, emoji="⭐")
        count = reaction.count if reaction else 1
        threshold = settings.get("starboard_threshold", 3)

        if count < threshold:
            return

        entry = await StarboardModel.get_entry(self.bot.db, message.id)
        embed = discord.Embed(
            description=message.content,
            color=0xF1C40F,
            timestamp=message.created_at
        )
        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
        embed.add_field(name="Source", value=f"[Jump to Message]({message.jump_url})")

        if message.attachments:
            embed.set_image(url=message.attachments[0].url)

        content = f"⭐ **{count}** | {message.channel.mention}"

        if entry and entry.get("starboard_message_id"):
            try:
                sb_msg = await sb_channel.fetch_message(entry["starboard_message_id"])
                await sb_msg.edit(content=content, embed=embed)
                await StarboardModel.update_stars(self.bot.db, message.id, count)
            except discord.NotFound:
                pass
        else:
            sb_msg = await sb_channel.send(content=content, embed=embed)
            await StarboardModel.create_entry(
                self.bot.db, message.id, guild.id, message.channel.id, message.author.id, sb_msg.id, count
            )


async def setup(bot):
    await bot.add_cog(Community(bot))

