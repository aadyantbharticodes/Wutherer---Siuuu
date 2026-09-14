from __future__ import annotations
import time
import asyncio
import logging
from collections import defaultdict
from typing import Optional, Any
import discord

from database.pool import DatabasePool
from database.models.antinuke import AntiNukeModel

log = logging.getLogger("wutherer.antinuke")


class AntiNukeService:
    def __init__(self, bot, db: DatabasePool):
        self.bot = bot
        self.db = db
        self._action_records: dict[str, list[float]] = defaultdict(list)

    def _get_key(self, guild_id: int, user_id: int, action: str) -> str:
        return f"{guild_id}:{user_id}:{action}"

    def record_action(self, guild_id: int, user_id: int, action: str, window_seconds: int = 15) -> int:
        key = self._get_key(guild_id, user_id, action)
        now = time.time()
        self._action_records[key] = [t for t in self._action_records[key] if now - t <= window_seconds]
        self._action_records[key].append(now)
        return len(self._action_records[key])

    async def check_violation(
        self,
        guild: discord.Guild,
        user_id: int,
        action: str,
        threshold: int
    ) -> bool:
        if user_id == guild.owner_id or user_id == self.bot.user.id:
            return False

        is_wl = await AntiNukeModel.is_whitelisted(self.db, guild.id, user_id)
        if is_wl:
            return False

        cfg = await AntiNukeModel.get_config(self.db, guild.id)
        if not cfg.get("enabled"):
            return False

        window = cfg.get("rate_window_seconds", 15)
        count = self.record_action(guild.id, user_id, action, window)
        if count >= threshold:
            action_type = cfg.get("action_type", "ban")
            await self.punish_culprit(guild, user_id, action, count, action_type)
            return True
        return False

    async def punish_culprit(
        self,
        guild: discord.Guild,
        user_id: int,
        reason_action: str,
        occurrences: int,
        action_type: str = "ban"
    ) -> None:
        member = guild.get_member(user_id)
        action_msg = "Unknown"
        cfg = await AntiNukeModel.get_config(self.db, guild.id)

        try:
            if action_type == "ban":
                await guild.ban(
                    discord.Object(id=user_id),
                    reason=f"Wutherer Anti-Nuke: Triggered {reason_action} limit ({occurrences} events)"
                )
                action_msg = "Banned"
            elif action_type == "kick" and member:
                await member.kick(
                    reason=f"Wutherer Anti-Nuke: Triggered {reason_action} limit ({occurrences} events)"
                )
                action_msg = "Kicked"
            elif action_type == "quarantine" and member:
                quarantine_role_id = cfg.get("quarantine_role_id")
                q_role = guild.get_role(quarantine_role_id) if quarantine_role_id else None
                if q_role:
                    roles_to_remove = [r for r in member.roles if not r.is_default() and not r.managed]
                    await member.remove_roles(*roles_to_remove, reason="Wutherer Anti-Nuke: Quarantine")
                    await member.add_roles(q_role, reason="Wutherer Anti-Nuke: Quarantine")
                    action_msg = "Quarantined"
                else:
                    await member.edit(roles=[], reason="Wutherer Anti-Nuke: Strip Roles")
                    action_msg = "Stripped All Roles"
            else:
                if member:
                    await member.edit(roles=[], reason="Wutherer Anti-Nuke: Strip Roles")
                    action_msg = "Stripped All Roles"
        except Exception as err:
            log.error("Failed to punish culprit %s in guild %s: %s", user_id, guild.id, err)
            action_msg = f"Failed ({err})"

        await AntiNukeModel.add_log(
            self.db,
            guild.id,
            user_id,
            reason_action,
            f"Triggered threshold with {occurrences} events within window",
            action_msg
        )

        log_ch_id = cfg.get("log_channel_id")
        if log_ch_id:
            channel = guild.get_channel(log_ch_id)
            if isinstance(channel, discord.TextChannel):
                embed = discord.Embed(
                    title="🚨 Anti-Nuke Threat Intercepted",
                    color=0xED4245,
                    description=f"Wutherer detected malicious mass activity and executed automated countermeasures."
                )
                embed.add_field(name="Culprit", value=f"<@{user_id}> (`{user_id}`)", inline=True)
                embed.add_field(name="Violation", value=f"`{reason_action}` ({occurrences} actions)", inline=True)
                embed.add_field(name="Action Taken", value=f"**{action_msg}**", inline=True)
                embed.set_footer(text="Wutherer Defense Core", icon_url=self.bot.user.display_avatar.url if self.bot.user else None)
                try:
                    await channel.send(embed=embed)
                except Exception:
                    pass

    async def panic_lockdown(self, guild: discord.Guild) -> dict:
        results = {"channels_locked": 0, "errors": []}
        everyone = guild.default_role

        for ch in guild.channels:
            if not isinstance(ch, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel)):
                continue

            current_ow = ch.overwrites_for(everyone)
            save_dict = {
                "send_messages": current_ow.send_messages,
                "send_messages_in_threads": current_ow.send_messages_in_threads,
                "create_public_threads": current_ow.create_public_threads,
                "connect": current_ow.connect,
                "add_reactions": current_ow.add_reactions
            }
            await AntiNukeModel.save_lockdown_state(self.db, guild.id, ch.id, save_dict)

            try:
                if isinstance(ch, discord.TextChannel):
                    await ch.set_permissions(
                        everyone,
                        send_messages=False,
                        send_messages_in_threads=False,
                        create_public_threads=False,
                        add_reactions=False,
                        reason="Wutherer Emergency Panic Lockdown"
                    )
                elif isinstance(ch, discord.VoiceChannel):
                    await ch.set_permissions(
                        everyone,
                        connect=False,
                        reason="Wutherer Emergency Panic Lockdown"
                    )
                results["channels_locked"] += 1
                await asyncio.sleep(0.3)
            except Exception as exc:
                results["errors"].append(f"Channel {ch.name}: {exc}")

        await AntiNukeModel.update_config(self.db, guild.id, panic_lockdown_enabled=1)
        return results

    async def lift_lockdown(self, guild: discord.Guild) -> dict:
        results = {"channels_unlocked": 0, "errors": []}
        everyone = guild.default_role
        saved_states = await AntiNukeModel.get_lockdown_states(self.db, guild.id)
        state_map = {s["channel_id"]: s["overwrites"] for s in saved_states}

        for ch in guild.channels:
            if ch.id not in state_map:
                continue
            ow_data = state_map[ch.id]
            try:
                ow = ch.overwrites_for(everyone)
                ow.send_messages = ow_data.get("send_messages")
                ow.send_messages_in_threads = ow_data.get("send_messages_in_threads")
                ow.create_public_threads = ow_data.get("create_public_threads")
                ow.connect = ow_data.get("connect")
                ow.add_reactions = ow_data.get("add_reactions")
                await ch.set_permissions(everyone, overwrite=ow, reason="Wutherer Lockdown Lifted")
                results["channels_unlocked"] += 1
                await asyncio.sleep(0.3)
            except Exception as exc:
                results["errors"].append(f"Channel {ch.name}: {exc}")

        await AntiNukeModel.clear_lockdown_states(self.db, guild.id)
        await AntiNukeModel.update_config(self.db, guild.id, panic_lockdown_enabled=0)
        return results
