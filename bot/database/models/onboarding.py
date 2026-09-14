from __future__ import annotations
import json
from typing import Optional, Any
from database.pool import DatabasePool


class AutoDMModel:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM autodm_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute("INSERT OR IGNORE INTO autodm_config (guild_id) VALUES (?)", guild_id)
            await db.commit()
            row = await db.fetchrow("SELECT * FROM autodm_config WHERE guild_id = ?", guild_id)
        res = dict(row) if row else {
            "guild_id": guild_id,
            "enabled": 0,
            "message": "Welcome to **{guild.name}**, {user.mention}! Please make sure to check out the rules.",
            "embed_json": None,
            "buttons_json": None,
            "delay_seconds": 0
        }
        try:
            res["embed"] = json.loads(res["embed_json"]) if res.get("embed_json") else None
        except Exception:
            res["embed"] = None
        try:
            res["buttons"] = json.loads(res["buttons_json"]) if res.get("buttons_json") else []
        except Exception:
            res["buttons"] = []
        return res

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        if "embed" in kwargs:
            kwargs["embed_json"] = json.dumps(kwargs.pop("embed")) if kwargs["embed"] else None
        if "buttons" in kwargs:
            kwargs["buttons_json"] = json.dumps(kwargs.pop("buttons")) if kwargs["buttons"] else None
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE autodm_config SET {sets} WHERE guild_id = ?", *vals)
        await db.commit()


class AutoPingModel:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM autoping_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute("INSERT OR IGNORE INTO autoping_config (guild_id) VALUES (?)", guild_id)
            await db.commit()
            row = await db.fetchrow("SELECT * FROM autoping_config WHERE guild_id = ?", guild_id)
        res = dict(row) if row else {
            "guild_id": guild_id,
            "enabled": 0,
            "channel_ids": "[]",
            "delete_after_seconds": 5,
            "ping_mode": "ghost",
            "message_template": "Welcome {user.mention} to {guild.name}!"
        }
        try:
            res["channels"] = json.loads(res["channel_ids"]) if res.get("channel_ids") else []
        except Exception:
            res["channels"] = []
        return res

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        if "channels" in kwargs:
            kwargs["channel_ids"] = json.dumps(kwargs.pop("channels"))
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE autoping_config SET {sets} WHERE guild_id = ?", *vals)
        await db.commit()


class AdvancedWelcomeModel:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchrow("SELECT * FROM advanced_welcome_config WHERE guild_id = ?", guild_id)
        if not row:
            await db.execute("INSERT OR IGNORE INTO advanced_welcome_config (guild_id) VALUES (?)", guild_id)
            await db.commit()
            row = await db.fetchrow("SELECT * FROM advanced_welcome_config WHERE guild_id = ?", guild_id)
        res = dict(row) if row else {
            "guild_id": guild_id,
            "multi_channels_json": "[]",
            "autorole_delay_minutes": 0,
            "autorole_delay_ids": "[]",
            "farewell_enabled": 0,
            "farewell_channel_id": None,
            "farewell_message": "Goodbye {user.name}, we hope to see you again!",
            "farewell_embed_json": None
        }
        try:
            res["multi_channels"] = json.loads(res["multi_channels_json"]) if res.get("multi_channels_json") else []
        except Exception:
            res["multi_channels"] = []
        try:
            res["autorole_delay_roles"] = json.loads(res["autorole_delay_ids"]) if res.get("autorole_delay_ids") else []
        except Exception:
            res["autorole_delay_roles"] = []
        try:
            res["farewell_embed"] = json.loads(res["farewell_embed_json"]) if res.get("farewell_embed_json") else None
        except Exception:
            res["farewell_embed"] = None
        return res

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **kwargs) -> None:
        if not kwargs:
            return
        if "multi_channels" in kwargs:
            kwargs["multi_channels_json"] = json.dumps(kwargs.pop("multi_channels"))
        if "autorole_delay_roles" in kwargs:
            kwargs["autorole_delay_ids"] = json.dumps(kwargs.pop("autorole_delay_roles"))
        if "farewell_embed" in kwargs:
            kwargs["farewell_embed_json"] = json.dumps(kwargs.pop("farewell_embed")) if kwargs["farewell_embed"] else None
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [guild_id]
        await db.execute(f"UPDATE advanced_welcome_config SET {sets} WHERE guild_id = ?", *vals)
        await db.commit()
