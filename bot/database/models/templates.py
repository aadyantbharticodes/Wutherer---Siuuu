from __future__ import annotations
import json
import uuid
import time
from typing import Optional, Any
from database.pool import DatabasePool


class ServerTemplateModel:
    @staticmethod
    async def create(
        db: DatabasePool,
        guild_id: int,
        creator_id: int,
        name: str,
        description: str,
        data: dict,
        is_public: bool = False,
        category: str = "general",
        template_id: Optional[str] = None
    ) -> str:
        tid = template_id or str(uuid.uuid4())[:8]
        await db.execute(
            """INSERT INTO server_templates (id, guild_id, creator_id, name, description, is_public, category, data_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            tid,
            guild_id,
            creator_id,
            name,
            description,
            1 if is_public else 0,
            category,
            json.dumps(data)
        )
        await db.commit()
        return tid

    @staticmethod
    async def get(db: DatabasePool, template_id: str) -> Optional[dict]:
        row = await db.fetchrow("SELECT * FROM server_templates WHERE id = ?", template_id)
        if not row:
            return None
        res = dict(row)
        try:
            res["data"] = json.loads(res["data_json"])
        except Exception:
            res["data"] = {}
        return res

    @staticmethod
    async def list_guild(db: DatabasePool, guild_id: int) -> list[dict]:
        rows = await db.fetch("SELECT * FROM server_templates WHERE guild_id = ? ORDER BY created_at DESC", guild_id)
        result = []
        for r in rows:
            item = dict(r)
            try:
                item["data"] = json.loads(item["data_json"])
            except Exception:
                item["data"] = {}
            result.append(item)
        return result

    @staticmethod
    async def list_public(db: DatabasePool, category: Optional[str] = None) -> list[dict]:
        if category:
            rows = await db.fetch(
                "SELECT * FROM server_templates WHERE is_public = 1 AND category = ? ORDER BY usage_count DESC",
                category
            )
        else:
            rows = await db.fetch("SELECT * FROM server_templates WHERE is_public = 1 ORDER BY usage_count DESC")
        result = []
        for r in rows:
            item = dict(r)
            try:
                item["data"] = json.loads(item["data_json"])
            except Exception:
                item["data"] = {}
            result.append(item)
        return result

    @staticmethod
    async def increment_usage(db: DatabasePool, template_id: str) -> None:
        await db.execute("UPDATE server_templates SET usage_count = usage_count + 1 WHERE id = ?", template_id)
        await db.commit()

    @staticmethod
    async def delete(db: DatabasePool, template_id: str, guild_id: Optional[int] = None) -> bool:
        if guild_id:
            res = await db.execute("DELETE FROM server_templates WHERE id = ? AND guild_id = ?", template_id, guild_id)
        else:
            res = await db.execute("DELETE FROM server_templates WHERE id = ?", template_id)
        await db.commit()
        return True

    @staticmethod
    async def update_visibility(db: DatabasePool, template_id: str, is_public: bool) -> None:
        await db.execute("UPDATE server_templates SET is_public = ? WHERE id = ?", 1 if is_public else 0, template_id)
        await db.commit()
