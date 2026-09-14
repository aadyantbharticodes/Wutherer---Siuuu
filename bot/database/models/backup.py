from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import aiosqlite


@dataclass
class GuildBackupSnapshot:
    backup_id: str
    guild_id: int
    guild_name: str
    created_by: int
    created_at: int = field(default_factory=lambda: int(time.time()))
    roles_data: List[Dict[str, Any]] = field(default_factory=list)
    categories_data: List[Dict[str, Any]] = field(default_factory=list)
    channels_data: List[Dict[str, Any]] = field(default_factory=list)
    emojis_data: List[Dict[str, Any]] = field(default_factory=list)
    bot_settings: Dict[str, Any] = field(default_factory=dict)
    notes: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, data_str: str) -> GuildBackupSnapshot:
        raw = json.loads(data_str)
        return cls(**raw)


class BackupModel:

    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def create_backup(self, snapshot: GuildBackupSnapshot) -> str:
        query = """
            INSERT INTO guild_backups (
                backup_id, guild_id, guild_name, created_by, created_at,
                roles_json, categories_json, channels_json, emojis_json,
                settings_json, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        await self.db.execute(
            query,
            (
                snapshot.backup_id,
                snapshot.guild_id,
                snapshot.guild_name,
                snapshot.created_by,
                snapshot.created_at,
                json.dumps(snapshot.roles_data),
                json.dumps(snapshot.categories_data),
                json.dumps(snapshot.channels_data),
                json.dumps(snapshot.emojis_data),
                json.dumps(snapshot.bot_settings),
                snapshot.notes,
            ),
        )
        await self.db.commit()
        return snapshot.backup_id

    async def get_backup(self, backup_id: str) -> Optional[GuildBackupSnapshot]:
        query = "SELECT * FROM guild_backups WHERE backup_id = ?"
        async with self.db.execute(query, (backup_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            return self._row_to_snapshot(row)

    async def list_guild_backups(self, guild_id: int, limit: int = 20) -> List[GuildBackupSnapshot]:
        query = """
            SELECT * FROM guild_backups 
            WHERE guild_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        """
        async with self.db.execute(query, (guild_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [self._row_to_snapshot(row) for row in rows]

    async def delete_backup(self, backup_id: str, guild_id: int) -> bool:
        query = "DELETE FROM guild_backups WHERE backup_id = ? AND guild_id = ?"
        cursor = await self.db.execute(query, (backup_id, guild_id))
        await self.db.commit()
        return cursor.rowcount > 0

    async def count_backups(self, guild_id: int) -> int:
        query = "SELECT COUNT(*) FROM guild_backups WHERE guild_id = ?"
        async with self.db.execute(query, (guild_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

    def _row_to_snapshot(self, row: Any) -> GuildBackupSnapshot:
        return GuildBackupSnapshot(
            backup_id=row[0],
            guild_id=row[1],
            guild_name=row[2],
            created_by=row[3],
            created_at=row[4],
            roles_data=json.loads(row[5]) if row[5] else [],
            categories_data=json.loads(row[6]) if row[6] else [],
            channels_data=json.loads(row[7]) if row[7] else [],
            emojis_data=json.loads(row[8]) if row[8] else [],
            bot_settings=json.loads(row[9]) if row[9] else {},
            notes=row[10],
        )

