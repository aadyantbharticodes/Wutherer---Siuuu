from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, List, Optional
import aiosqlite


@dataclass
class AntiPhishingConfig:
    guild_id: int
    enabled: bool = True
    action: str = "timeout"
    timeout_duration: int = 3600
    log_channel_id: Optional[int] = None
    whitelisted_domains: List[str] = field(default_factory=lambda: ["discord.com", "discord.gg", "youtube.com", "github.com", "google.com"])
    custom_blacklisted_domains: List[str] = field(default_factory=list)
    alert_staff: bool = True


class AntiPhishingModel:

    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def get_config(self, guild_id: int) -> AntiPhishingConfig:
        query = "SELECT * FROM antiphishing_configs WHERE guild_id = ?"
        async with self.db.execute(query, (guild_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return AntiPhishingConfig(guild_id=guild_id)
            return self._row_to_config(row)

    async def save_config(self, config: AntiPhishingConfig) -> None:
        query = """
            INSERT INTO antiphishing_configs (
                guild_id, enabled, action, timeout_duration, log_channel_id,
                whitelist_json, blacklist_json, alert_staff
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                enabled = excluded.enabled,
                action = excluded.action,
                timeout_duration = excluded.timeout_duration,
                log_channel_id = excluded.log_channel_id,
                whitelist_json = excluded.whitelist_json,
                blacklist_json = excluded.blacklist_json,
                alert_staff = excluded.alert_staff
        """
        await self.db.execute(
            query,
            (
                config.guild_id,
                1 if config.enabled else 0,
                config.action,
                config.timeout_duration,
                config.log_channel_id,
                json.dumps(config.whitelisted_domains),
                json.dumps(config.custom_blacklisted_domains),
                1 if config.alert_staff else 0,
            ),
        )
        await self.db.commit()

    async def add_whitelist_domain(self, guild_id: int, domain: str) -> bool:
        cfg = await self.get_config(guild_id)
        d = domain.lower().strip()
        if d not in cfg.whitelisted_domains:
            cfg.whitelisted_domains.append(d)
            await self.save_config(cfg)
            return True
        return False

    async def remove_whitelist_domain(self, guild_id: int, domain: str) -> bool:
        cfg = await self.get_config(guild_id)
        d = domain.lower().strip()
        if d in cfg.whitelisted_domains:
            cfg.whitelisted_domains.remove(d)
            await self.save_config(cfg)
            return True
        return False

    def _row_to_config(self, row: Any) -> AntiPhishingConfig:
        return AntiPhishingConfig(
            guild_id=row[0],
            enabled=bool(row[1]),
            action=row[2],
            timeout_duration=row[3],
            log_channel_id=row[4],
            whitelisted_domains=json.loads(row[5]) if row[5] else ["discord.com", "discord.gg"],
            custom_blacklisted_domains=json.loads(row[6]) if row[6] else [],
            alert_staff=bool(row[7]),
        )

