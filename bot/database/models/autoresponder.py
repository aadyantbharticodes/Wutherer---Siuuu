from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import aiosqlite


@dataclass
class AutoResponseTrigger:
    trigger_id: int
    guild_id: int
    trigger_text: str
    response_text: str
    match_mode: str = "exact"
    is_embed: bool = False
    embed_color: Optional[int] = None
    cooldown_seconds: int = 5
    delete_trigger: bool = False
    enabled: bool = True
    created_by: int = 0
    created_at: int = field(default_factory=lambda: int(time.time()))
    uses_count: int = 0


class AutoResponderModel:

    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def add_trigger(
        self,
        guild_id: int,
        trigger_text: str,
        response_text: str,
        match_mode: str = "exact",
        is_embed: bool = False,
        embed_color: Optional[int] = None,
        cooldown_seconds: int = 5,
        delete_trigger: bool = False,
        created_by: int = 0,
    ) -> int:
        query = """
            INSERT INTO autoresponders (
                guild_id, trigger_text, response_text, match_mode,
                is_embed, embed_color, cooldown_seconds, delete_trigger,
                enabled, created_by, created_at, uses_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, 0)
        """
        now = int(time.time())
        cursor = await self.db.execute(
            query,
            (
                guild_id,
                trigger_text.lower() if match_mode != "regex" else trigger_text,
                response_text,
                match_mode,
                1 if is_embed else 0,
                embed_color,
                cooldown_seconds,
                1 if delete_trigger else 0,
                created_by,
                now,
            ),
        )
        await self.db.commit()
        return cursor.lastrowid

    async def get_trigger(self, trigger_id: int, guild_id: int) -> Optional[AutoResponseTrigger]:
        query = "SELECT * FROM autoresponders WHERE trigger_id = ? AND guild_id = ?"
        async with self.db.execute(query, (trigger_id, guild_id)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            return self._row_to_trigger(row)

    async def list_triggers(self, guild_id: int) -> List[AutoResponseTrigger]:
        query = "SELECT * FROM autoresponders WHERE guild_id = ? ORDER BY trigger_id ASC"
        async with self.db.execute(query, (guild_id,)) as cursor:
            rows = await cursor.fetchall()
            return [self._row_to_trigger(r) for r in rows]

    async def delete_trigger(self, trigger_id: int, guild_id: int) -> bool:
        query = "DELETE FROM autoresponders WHERE trigger_id = ? AND guild_id = ?"
        cursor = await self.db.execute(query, (trigger_id, guild_id))
        await self.db.commit()
        return cursor.rowcount > 0

    async def set_enabled(self, trigger_id: int, guild_id: int, enabled: bool) -> bool:
        query = "UPDATE autoresponders SET enabled = ? WHERE trigger_id = ? AND guild_id = ?"
        cursor = await self.db.execute(query, (1 if enabled else 0, trigger_id, guild_id))
        await self.db.commit()
        return cursor.rowcount > 0

    async def increment_uses(self, trigger_id: int) -> None:
        query = "UPDATE autoresponders SET uses_count = uses_count + 1 WHERE trigger_id = ?"
        await self.db.execute(query, (trigger_id,))
        await self.db.commit()

    def _row_to_trigger(self, row: Any) -> AutoResponseTrigger:
        return AutoResponseTrigger(
            trigger_id=row[0],
            guild_id=row[1],
            trigger_text=row[2],
            response_text=row[3],
            match_mode=row[4],
            is_embed=bool(row[5]),
            embed_color=row[6],
            cooldown_seconds=row[7],
            delete_trigger=bool(row[8]),
            enabled=bool(row[9]),
            created_by=row[10],
            created_at=row[11],
            uses_count=row[12],
        )

