from __future__ import annotations
import time
import logging
from datetime import datetime, timezone
import discord

from database.pool import DatabasePool
from database.models.antialt import AntiAltModel

log = logging.getLogger("wutherer.antialt")


class AntiAltService:
    def __init__(self, bot, db: DatabasePool):
        self.bot = bot
        self.db = db

    async def verify_member(self, member: discord.Member) -> bool:
        if member.bot:
            return True

        cfg = await AntiAltModel.get_config(self.db, member.guild.id)
        if not cfg.get("enabled"):
            return True

        now = datetime.now(timezone.utc)
        account_age = (now - member.created_at).days
        min_age = cfg.get("min_age_days", 7)
        require_avatar = bool(cfg.get("require_avatar", 0))

        failed_reasons = []
        if account_age < min_age:
            failed_reasons.append(f"Account age ({account_age}d) is below minimum {min_age}d threshold")

        if require_avatar and member.avatar is None:
            failed_reasons.append("Default Discord avatar detected (custom avatar required)")

        if not failed_reasons:
            return True

        action = cfg.get("action_type", "quarantine")
        reason_str = "; ".join(failed_reasons)
        action_taken = "Failed"

        try:
            if action == "ban":
                await member.ban(reason=f"Sentinel Anti-Alt: {reason_str}")
                action_taken = "Banned"
            elif action == "kick":
                await member.kick(reason=f"Sentinel Anti-Alt: {reason_str}")
                action_taken = "Kicked"
            elif action == "quarantine":
                q_role = discord.utils.get(member.guild.roles, name="Quarantined")
                if q_role:
                    await member.add_roles(q_role, reason=f"Sentinel Anti-Alt: {reason_str}")
                    action_taken = "Quarantined"
                else:
                    await member.kick(reason=f"Sentinel Anti-Alt: {reason_str}")
                    action_taken = "Kicked (No Quarantine Role)"
        except Exception as e:
            log.error("Failed executing anti-alt action on %s: %s", member.id, e)
            action_taken = f"Error ({e})"

        await AntiAltModel.add_log(
            self.db,
            member.guild.id,
            member.id,
            account_age,
            action_taken,
            reason_str
        )

        log_ch_id = cfg.get("log_channel_id")
        if log_ch_id:
            channel = member.guild.get_channel(log_ch_id)
            if isinstance(channel, discord.TextChannel):
                embed = discord.Embed(
                    title="🛡️ Anti-Alt Protection Triggered",
                    color=0xED4245,
                    description=f"{member.mention} (`{member.id}`) flagged as suspicious account."
                )
                embed.add_field(name="Account Age", value=f"**{account_age}** day(s)", inline=True)
                embed.add_field(name="Action Taken", value=f"**{action_taken}**", inline=True)
                embed.add_field(name="Violation", value=reason_str, inline=False)
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text="Sentinel Security Core")
                try:
                    await channel.send(embed=embed)
                except Exception:
                    pass

        return False
