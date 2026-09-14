from __future__ import annotations
import logging
import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_NAME, BOT_COLOR_ERROR, BOT_COLOR_SUCCESS, DEFAULT_PREFIX
from database.models.guild import GuildSettings, WelcomeConfig, Autoroles

log = logging.getLogger("wutherer.events")


class Events(WuthererCog):

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("%s is online! Connected as %s (ID: %s)", BOT_NAME, self.bot.user, self.bot.user.id)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        log.info("Joined guild: %s (ID: %s, Members: %s)", guild.name, guild.id, guild.member_count)
        await GuildSettings.get(self.bot.db, guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        log.info("Left guild: %s (ID: %s)", guild.name, guild.id)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not member.guild:
            return


        target = "bot" if member.bot else "human"
        autoroles = await Autoroles.get(self.bot.db, member.guild.id)
        for ar in autoroles:
            if ar.get("target") in ("all", target):
                role = member.guild.get_role(ar["role_id"])
                if role and member.guild.me.guild_permissions.manage_roles and role < member.guild.me.top_role:
                    try:
                        await member.add_roles(role, reason="Sentinel Autorole")
                    except discord.HTTPException:
                        pass


        w_cfg = await WelcomeConfig.get(self.bot.db, member.guild.id)
        if w_cfg.get("enabled") and w_cfg.get("channel_id"):
            channel = member.guild.get_channel(w_cfg["channel_id"])
            if channel and channel.permissions_for(member.guild.me).send_messages:
                msg_template = w_cfg.get("message") or "Welcome to **{server}**, {mention}!"
                msg = msg_template.replace("{mention}", member.mention)
                msg = msg.replace("{user}", str(member))
                msg = msg.replace("{server}", member.guild.name)
                msg = msg.replace("{count}", str(member.guild.member_count))
                embed = discord.Embed(
                    description=msg,
                    color=0x6C5CE7,
                    timestamp=discord.utils.utcnow()
                )
                embed.set_author(name=f"Welcome {member.display_name}!", icon_url=member.display_avatar.url)
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f"Member #{member.guild.member_count}")
                try:
                    await channel.send(embed=embed)
                except discord.HTTPException:
                    pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if not member.guild:
            return

        w_cfg = await WelcomeConfig.get(self.bot.db, member.guild.id)
        if w_cfg.get("goodbye_enabled") and w_cfg.get("goodbye_channel_id"):
            channel = member.guild.get_channel(w_cfg["goodbye_channel_id"])
            if channel and channel.permissions_for(member.guild.me).send_messages:
                msg_template = w_cfg.get("goodbye_message") or "**{user}** has left the server."
                msg = msg_template.replace("{user}", str(member))
                msg = msg.replace("{server}", member.guild.name)
                embed = discord.Embed(
                    description=msg,
                    color=0xE74C3C,
                    timestamp=discord.utils.utcnow()
                )
                try:
                    await channel.send(embed=embed)
                except discord.HTTPException:
                    pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):

        if hasattr(ctx.command, "on_error"):
            return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, "original", error)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.MissingPermissions):
            missing = ", ".join(f"`{p}`" for p in error.missing_permissions)
            return await ctx.send(embed=discord.Embed(
                description=f"❌ You are missing required permissions: {missing}",
                color=BOT_COLOR_ERROR
            ))

        if isinstance(error, commands.BotMissingPermissions):
            missing = ", ".join(f"`{p}`" for p in error.missing_permissions)
            return await ctx.send(embed=discord.Embed(
                description=f"❌ I lack required permissions to execute this: {missing}",
                color=BOT_COLOR_ERROR
            ))

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=discord.Embed(
                description=f"⏳ This command is on cooldown. Try again in **{error.retry_after:.1f}s**.",
                color=BOT_COLOR_ERROR
            ))

        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument)):
            return await ctx.send(embed=discord.Embed(
                description=f"⚠️ Invalid arguments. Usage: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`",
                color=BOT_COLOR_ERROR
            ))

        if isinstance(error, commands.CheckFailure):
            return await ctx.send(embed=discord.Embed(
                description=f"❌ {error}",
                color=BOT_COLOR_ERROR
            ))

        log.error("Command error in '%s': %s", ctx.command.qualified_name if ctx.command else "Unknown", error, exc_info=True)
        await ctx.send(embed=discord.Embed(
            description=f"❌ An unexpected error occurred while executing this command.",
            color=BOT_COLOR_ERROR
        ))


async def setup(bot):
    await bot.add_cog(Events(bot))

