from __future__ import annotations
import asyncio
import logging
from typing import Optional, Any
import discord

from database.pool import DatabasePool
from database.models.onboarding import AutoDMModel, AutoPingModel, AdvancedWelcomeModel

log = logging.getLogger("wutherer.onboarding")


class OnboardingService:
    @staticmethod
    def interpolate(text: str, member: discord.Member) -> str:
        if not text:
            return ""
        guild = member.guild
        owner = guild.owner
        replacements = {
            "{user}": str(member),
            "{user.mention}": member.mention,
            "{user.name}": member.name,
            "{user.id}": str(member.id),
            "{user.created_at}": member.created_at.strftime("%Y-%m-%d"),
            "{guild.name}": guild.name,
            "{guild.id}": str(guild.id),
            "{guild.member_count}": str(guild.member_count),
            "{owner.name}": owner.name if owner else "Owner",
            "{owner.mention}": owner.mention if owner else "@owner",
        }
        res = text
        for placeholder, val in replacements.items():
            res = res.replace(placeholder, val)
        return res

    @staticmethod
    def build_embed(embed_data: dict, member: discord.Member) -> discord.Embed:
        title = OnboardingService.interpolate(embed_data.get("title", ""), member)
        desc = OnboardingService.interpolate(embed_data.get("description", ""), member)
        color = embed_data.get("color", 0x5865F2)
        embed = discord.Embed(title=title or None, description=desc or None, color=color)

        if embed_data.get("thumbnail_avatar"):
            embed.set_thumbnail(url=member.display_avatar.url)
        elif embed_data.get("thumbnail_url"):
            embed.set_thumbnail(url=embed_data["thumbnail_url"])

        if embed_data.get("image_url"):
            embed.set_image(url=embed_data["image_url"])

        if embed_data.get("footer"):
            f_text = OnboardingService.interpolate(embed_data["footer"], member)
            embed.set_footer(text=f_text)

        for f in embed_data.get("fields", []):
            name = OnboardingService.interpolate(f.get("name", ""), member)
            val = OnboardingService.interpolate(f.get("value", ""), member)
            embed.add_field(name=name, value=val, inline=f.get("inline", False))

        return embed

    @staticmethod
    def build_buttons(buttons_data: list[dict]) -> Optional[discord.ui.View]:
        if not buttons_data:
            return None
        view = discord.ui.View(timeout=None)
        for b in buttons_data:
            label = b.get("label", "Link")
            url = b.get("url")
            emoji = b.get("emoji")
            if url:
                btn = discord.ui.Button(label=label, url=url, emoji=emoji)
                view.add_item(btn)
        return view if len(view.children) > 0 else None

    @staticmethod
    async def dispatch_auto_dm(bot, db: DatabasePool, member: discord.Member) -> bool:
        cfg = await AutoDMModel.get(db, member.guild.id)
        if not cfg.get("enabled"):
            return False

        delay = cfg.get("delay_seconds", 0)
        if delay > 0:
            await asyncio.sleep(delay)

        message_text = OnboardingService.interpolate(cfg.get("message", ""), member)
        embed = None
        if cfg.get("embed"):
            try:
                embed = OnboardingService.build_embed(cfg["embed"], member)
            except Exception as e:
                log.error("Failed building AutoDM embed: %s", e)

        view = OnboardingService.build_buttons(cfg.get("buttons", []))

        try:
            kwargs = {}
            if message_text:
                kwargs["content"] = message_text
            if embed:
                kwargs["embed"] = embed
            if view:
                kwargs["view"] = view
            if kwargs:
                await member.send(**kwargs)
                return True
        except (discord.Forbidden, discord.HTTPException):
            log.debug("Could not DM member %s (DMs closed)", member.id)
        return False

    @staticmethod
    async def dispatch_auto_ping(bot, db: DatabasePool, member: discord.Member) -> None:
        cfg = await AutoPingModel.get(db, member.guild.id)
        if not cfg.get("enabled"):
            return

        channels = cfg.get("channels", [])
        if not channels:
            return

        mode = cfg.get("ping_mode", "ghost")
        delete_after = cfg.get("delete_after_seconds", 5)
        raw_msg = cfg.get("message_template", "Welcome {user.mention} to {guild.name}!")
        content = OnboardingService.interpolate(raw_msg, member)

        for ch_id in channels:
            ch = member.guild.get_channel(int(ch_id))
            if not isinstance(ch, discord.TextChannel):
                continue
            try:
                msg = await ch.send(content)
                if mode == "ghost" and delete_after > 0:
                    asyncio.create_task(OnboardingService._delete_delayed(msg, delete_after))
            except Exception as e:
                log.debug("Auto-ping failed in channel %s: %s", ch_id, e)

    @staticmethod
    async def _delete_delayed(message: discord.Message, delay: int) -> None:
        await asyncio.sleep(delay)
        try:
            await message.delete()
        except Exception:
            pass
