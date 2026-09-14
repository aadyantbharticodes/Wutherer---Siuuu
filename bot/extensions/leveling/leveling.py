from __future__ import annotations
import math
import random
import time
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from core.checks import is_admin, is_mod
from config import BOT_COLOR, BOT_COLOR_SUCCESS
from database.models.leveling import LevelingConfig, UserLevels, LevelRewards
from services.image import ImageService


class Leveling(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self._xp_cooldowns: dict[tuple[int, int], float] = {}

    @commands.command(name="rank", aliases=["level", "lvl"])
    async def view_rank(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        target = member or ctx.author
        if target.bot:
            return await ctx.send("Bots do not earn XP.")

        async with ctx.typing():
            user_data = await UserLevels.get(self.bot.db, ctx.guild.id, target.id)
            current_xp = user_data["xp"]
            current_lvl = user_data["level"]
            needed_xp = UserLevels.xp_for_level(current_lvl + 1)
            rank = await UserLevels.get_rank(self.bot.db, ctx.guild.id, target.id)

            avatar_img = None
            try:
                avatar_img = await ImageService.fetch_image(self.session, target.display_avatar.url)
            except Exception:
                pass

            card_buffer = ImageService.render_rank_card(
                username=target.display_name,
                avatar_img=avatar_img,
                level=current_lvl,
                xp=current_xp,
                xp_needed=needed_xp,
                rank=rank
            )

            file = discord.File(card_buffer, filename="rank.png")
            await ctx.send(file=file)

    @commands.command(name="leaderboard", aliases=["lb", "top"])
    async def view_leaderboard(self, ctx: commands.Context):
        top_users = await UserLevels.get_leaderboard(self.bot.db, ctx.guild.id, limit=10)
        if not top_users:
            return await ctx.send("No leveling data found in this server.")

        lines = []
        for i, u in enumerate(top_users):
            member = ctx.guild.get_member(u["user_id"])
            name = member.display_name if member else f"User {u['user_id']}"
            lines.append(f"**#{i+1}** {name} — Level **{u['level']}** ({u['xp']:,} XP)")

        embed = discord.Embed(
            title=f"🏆 XP Leaderboard — {ctx.guild.name}",
            description="\n".join(lines),
            color=BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="setxp")
    @is_admin()
    async def set_user_xp(self, ctx: commands.Context, member: discord.Member, xp: int):
        lvl = UserLevels.level_for_xp(xp)
        await UserLevels.set_xp(self.bot.db, ctx.guild.id, member.id, xp, lvl)
        await ctx.send(embed=discord.Embed(
            description=f"Set {member.mention}'s XP to **{xp:,}** (Level {lvl}).",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="addreward")
    @is_admin()
    async def add_level_reward(self, ctx: commands.Context, level: int, role: discord.Role):
        await LevelRewards.add(self.bot.db, ctx.guild.id, level, role.id)
        await ctx.send(embed=discord.Embed(
            description=f"Members reaching Level **{level}** will now receive {role.mention}.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        cfg = await LevelingConfig.get(self.bot.db, message.guild.id)
        if not cfg.get("enabled"):
            return

        key = (message.guild.id, message.author.id)
        now = time.time()
        if now - self._xp_cooldowns.get(key, 0) < 60:
            return
        self._xp_cooldowns[key] = now

        rate = cfg.get("xp_rate", 1.0)
        gain = int(random.randint(15, 25) * rate)

        leveled_up, new_level = await UserLevels.add_xp(self.bot.db, message.guild.id, message.author.id, gain)
        if leveled_up and cfg.get("announce_levelup"):
            target_chan = message.guild.get_channel(cfg.get("channel_id")) or message.channel
            if target_chan and target_chan.permissions_for(message.guild.me).send_messages:
                embed = discord.Embed(
                    description=f"🎉 Congratulations {message.author.mention}, you leveled up to **Level {new_level}**!",
                    color=BOT_COLOR_SUCCESS
                )
                try:
                    await target_chan.send(embed=embed)
                except discord.HTTPException:
                    pass


            reward_role_id = await LevelRewards.get_for_level(self.bot.db, message.guild.id, new_level)
            if reward_role_id:
                reward_role = message.guild.get_role(reward_role_id)
                if reward_role and message.guild.me.guild_permissions.manage_roles and reward_role < message.guild.me.top_role:
                    try:
                        await message.author.add_roles(reward_role, reason=f"Level {new_level} Reward")
                    except discord.HTTPException:
                        pass


async def setup(bot):
    await bot.add_cog(Leveling(bot))

