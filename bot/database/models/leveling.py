from __future__ import annotations
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.pool import DatabasePool


class LevelingConfig:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchone(
            "SELECT * FROM leveling_config WHERE guild_id = ?", (guild_id,)
        )
        if row:
            for key in ("ignored_channels", "ignored_roles"):
                if key in row and isinstance(row[key], str):
                    try:
                        row[key] = json.loads(row[key])
                    except json.JSONDecodeError:
                        row[key] = []
            return row
        return {"guild_id": guild_id, "enabled": 0, "xp_rate": 1.0}

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **fields) -> None:
        for key in ("ignored_channels", "ignored_roles"):
            if key in fields and isinstance(fields[key], list):
                fields[key] = json.dumps(fields[key])
        existing = await db.fetchone(
            "SELECT guild_id FROM leveling_config WHERE guild_id = ?", (guild_id,)
        )
        if not existing:
            await db.execute("INSERT INTO leveling_config (guild_id) VALUES (?)", (guild_id,))
        if fields:
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            values = list(fields.values()) + [guild_id]
            await db.execute(
                f"UPDATE leveling_config SET {set_clause} WHERE guild_id = ?", tuple(values)
            )
        await db.commit()


class UserLevel:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int, user_id: int) -> dict:
        row = await db.fetchone(
            "SELECT * FROM user_levels WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        return row or {"guild_id": guild_id, "user_id": user_id, "xp": 0, "level": 0, "messages": 0}

    @staticmethod
    async def add_xp(db: DatabasePool, guild_id: int, user_id: int, amount: int) -> dict:
        current = await UserLevel.get(db, guild_id, user_id)
        new_xp = current["xp"] + amount
        new_messages = current["messages"] + 1

        from config import LEVEL_FORMULA_BASE, LEVEL_FORMULA_MULTIPLIER
        new_level = current["level"]
        while new_xp >= int(LEVEL_FORMULA_BASE * (LEVEL_FORMULA_MULTIPLIER ** new_level)):
            new_xp -= int(LEVEL_FORMULA_BASE * (LEVEL_FORMULA_MULTIPLIER ** new_level))
            new_level += 1

        await db.execute(
            "INSERT INTO user_levels (guild_id, user_id, xp, level, messages, last_xp_at) "
            "VALUES (?, ?, ?, ?, ?, datetime('now')) "
            "ON CONFLICT(guild_id, user_id) DO UPDATE SET "
            "xp = ?, level = ?, messages = ?, last_xp_at = datetime('now')",
            (guild_id, user_id, new_xp, new_level, new_messages,
             new_xp, new_level, new_messages),
        )
        await db.commit()

        leveled_up = new_level > current["level"]
        return {"xp": new_xp, "level": new_level, "messages": new_messages, "leveled_up": leveled_up}

    @staticmethod
    async def get_leaderboard(db: DatabasePool, guild_id: int, limit: int = 10) -> list[dict]:
        return await db.fetchall(
            "SELECT * FROM user_levels WHERE guild_id = ? ORDER BY level DESC, xp DESC LIMIT ?",
            (guild_id, limit),
        )

    @staticmethod
    async def get_rank(db: DatabasePool, guild_id: int, user_id: int) -> int:
        return await db.fetchval(
            "SELECT COUNT(*) + 1 FROM user_levels WHERE guild_id = ? AND "
            "(level > (SELECT level FROM user_levels WHERE guild_id = ? AND user_id = ?) OR "
            "(level = (SELECT level FROM user_levels WHERE guild_id = ? AND user_id = ?) AND "
            "xp > (SELECT xp FROM user_levels WHERE guild_id = ? AND user_id = ?)))",
            (guild_id, guild_id, user_id, guild_id, user_id, guild_id, user_id),
            default=1,
        )

    @staticmethod
    async def set_level(db: DatabasePool, guild_id: int, user_id: int, level: int, xp: int = 0) -> None:
        await db.execute(
            "INSERT INTO user_levels (guild_id, user_id, level, xp) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(guild_id, user_id) DO UPDATE SET level = ?, xp = ?",
            (guild_id, user_id, level, xp, level, xp),
        )
        await db.commit()

    @staticmethod
    async def reset(db: DatabasePool, guild_id: int, user_id: int = None) -> None:
        if user_id:
            await db.execute(
                "DELETE FROM user_levels WHERE guild_id = ? AND user_id = ?",
                (guild_id, user_id),
            )
        else:
            await db.execute("DELETE FROM user_levels WHERE guild_id = ?", (guild_id,))
        await db.commit()


class LevelReward:
    @staticmethod
    async def get_all(db: DatabasePool, guild_id: int) -> list[dict]:
        return await db.fetchall(
            "SELECT * FROM level_rewards WHERE guild_id = ? ORDER BY level ASC",
            (guild_id,),
        )

    @staticmethod
    async def get_for_level(db: DatabasePool, guild_id: int, level: int) -> dict | None:
        return await db.fetchone(
            "SELECT * FROM level_rewards WHERE guild_id = ? AND level = ?",
            (guild_id, level),
        )

    @staticmethod
    async def set_reward(db: DatabasePool, guild_id: int, level: int, role_id: int) -> None:
        await db.execute(
            "INSERT INTO level_rewards (guild_id, level, role_id) VALUES (?, ?, ?) "
            "ON CONFLICT(guild_id, level) DO UPDATE SET role_id = ?",
            (guild_id, level, role_id, role_id),
        )
        await db.commit()

    @staticmethod
    async def remove(db: DatabasePool, guild_id: int, level: int) -> None:
        await db.execute(
            "DELETE FROM level_rewards WHERE guild_id = ? AND level = ?",
            (guild_id, level),
        )
        await db.commit()

