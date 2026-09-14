from __future__ import annotations
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from database.pool import DatabasePool


class ModerationDB:
    @staticmethod
    async def add_warning(db: DatabasePool, guild_id: int, user_id: int,
                          moderator_id: int, reason: str = None) -> int:
                              pass
        cursor = await db.execute(
            "INSERT INTO warnings (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (guild_id, user_id, moderator_id, reason),
        )
        await db.commit()
        return cursor.lastrowid

    @staticmethod
    async def get_warnings(db: DatabasePool, guild_id: int, user_id: int) -> list[dict]:
        return await db.fetchall(
            "SELECT * FROM warnings WHERE guild_id = ? AND user_id = ? ORDER BY created_at DESC",
            (guild_id, user_id),
        )

    @staticmethod
    async def count_warnings(db: DatabasePool, guild_id: int, user_id: int) -> int:
        return await db.fetchval(
            "SELECT COUNT(*) FROM warnings WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id), default=0,
        )

    @staticmethod
    async def clear_warnings(db: DatabasePool, guild_id: int, user_id: int) -> int:
        result = await db.execute(
            "DELETE FROM warnings WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        await db.commit()
        return result.rowcount

    @staticmethod
    async def remove_warning(db: DatabasePool, warning_id: int) -> bool:
        result = await db.execute("DELETE FROM warnings WHERE id = ?", (warning_id,))
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def add_case(db: DatabasePool, guild_id: int, user_id: int,
                       moderator_id: int, action: str, reason: str = None,
                       duration: int = None) -> int:
                           pass
        cursor = await db.execute(
            "INSERT INTO mod_cases (guild_id, user_id, moderator_id, action, reason, duration) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (guild_id, user_id, moderator_id, action, reason, duration),
        )
        await db.commit()
        return cursor.lastrowid

    @staticmethod
    async def get_cases(db: DatabasePool, guild_id: int, user_id: int = None,
                        limit: int = 50) -> list[dict]:
                            pass
        if user_id:
            return await db.fetchall(
                "SELECT * FROM mod_cases WHERE guild_id = ? AND user_id = ? "
                "ORDER BY created_at DESC LIMIT ?",
                (guild_id, user_id, limit),
            )
        return await db.fetchall(
            "SELECT * FROM mod_cases WHERE guild_id = ? ORDER BY created_at DESC LIMIT ?",
            (guild_id, limit),
        )

    @staticmethod
    async def add_note(db: DatabasePool, guild_id: int, user_id: int,
                       moderator_id: int, content: str) -> int:
                           pass
        cursor = await db.execute(
            "INSERT INTO mod_notes (guild_id, user_id, moderator_id, content) VALUES (?, ?, ?, ?)",
            (guild_id, user_id, moderator_id, content),
        )
        await db.commit()
        return cursor.lastrowid

    @staticmethod
    async def get_notes(db: DatabasePool, guild_id: int, user_id: int) -> list[dict]:
        return await db.fetchall(
            "SELECT * FROM mod_notes WHERE guild_id = ? AND user_id = ? ORDER BY created_at DESC",
            (guild_id, user_id),
        )

    @staticmethod
    async def add_tempban(db: DatabasePool, guild_id: int, user_id: int,
                          moderator_id: int, expires_at: str, reason: str = None) -> int:
                              pass
        cursor = await db.execute(
            "INSERT INTO tempbans (guild_id, user_id, moderator_id, reason, expires_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (guild_id, user_id, moderator_id, reason, expires_at),
        )
        await db.commit()
        return cursor.lastrowid

    @staticmethod
    async def get_expired_tempbans(db: DatabasePool) -> list[dict]:
        return await db.fetchall(
            "SELECT * FROM tempbans WHERE expires_at <= datetime('now')"
        )

    @staticmethod
    async def remove_tempban(db: DatabasePool, tempban_id: int) -> None:
        await db.execute("DELETE FROM tempbans WHERE id = ?", (tempban_id,))
        await db.commit()


class AutomodConfig:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchone(
            "SELECT * FROM automod_config WHERE guild_id = ?", (guild_id,)
        )
        if row:
            for key in ("antilink_whitelist", "badwords", "ignored_channels", "ignored_roles"):
                if key in row and isinstance(row[key], str):
                    try:
                        row[key] = json.loads(row[key])
                    except json.JSONDecodeError:
                        row[key] = []
            return row
        return {"guild_id": guild_id}

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **fields) -> None:
        for key in ("antilink_whitelist", "badwords", "ignored_channels", "ignored_roles"):
            if key in fields and isinstance(fields[key], (list, dict)):
                fields[key] = json.dumps(fields[key])

        existing = await db.fetchone(
            "SELECT guild_id FROM automod_config WHERE guild_id = ?", (guild_id,)
        )
        if not existing:
            await db.execute(
                "INSERT INTO automod_config (guild_id) VALUES (?)", (guild_id,)
            )

        if fields:
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            values = list(fields.values()) + [guild_id]
            await db.execute(
                f"UPDATE automod_config SET {set_clause} WHERE guild_id = ?",
                tuple(values),
            )
        await db.commit()


class AntinukeConfig:
    @staticmethod
    async def get(db: DatabasePool, guild_id: int) -> dict:
        row = await db.fetchone(
            "SELECT * FROM antinuke_config WHERE guild_id = ?", (guild_id,)
        )
        return row or {"guild_id": guild_id, "enabled": 0}

    @staticmethod
    async def update(db: DatabasePool, guild_id: int, **fields) -> None:
        existing = await db.fetchone(
            "SELECT guild_id FROM antinuke_config WHERE guild_id = ?", (guild_id,)
        )
        if not existing:
            await db.execute(
                "INSERT INTO antinuke_config (guild_id) VALUES (?)", (guild_id,)
            )
        if fields:
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            values = list(fields.values()) + [guild_id]
            await db.execute(
                f"UPDATE antinuke_config SET {set_clause} WHERE guild_id = ?",
                tuple(values),
            )
        await db.commit()

    @staticmethod
    async def is_whitelisted(db: DatabasePool, guild_id: int, user_id: int) -> bool:
        row = await db.fetchone(
            "SELECT 1 FROM antinuke_whitelist WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        return row is not None

    @staticmethod
    async def add_whitelist(db: DatabasePool, guild_id: int, user_id: int, added_by: int) -> None:
        await db.execute(
            "INSERT OR IGNORE INTO antinuke_whitelist (guild_id, user_id, added_by) VALUES (?, ?, ?)",
            (guild_id, user_id, added_by),
        )
        await db.commit()

    @staticmethod
    async def remove_whitelist(db: DatabasePool, guild_id: int, user_id: int) -> None:
        await db.execute(
            "DELETE FROM antinuke_whitelist WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        await db.commit()

    @staticmethod
    async def record_action(db: DatabasePool, guild_id: int, user_id: int, action: str) -> None:
        await db.execute(
            "INSERT INTO antinuke_actions (guild_id, user_id, action) VALUES (?, ?, ?)",
            (guild_id, user_id, action),
        )
        await db.commit()

    @staticmethod
    async def count_recent_actions(db: DatabasePool, guild_id: int, user_id: int,
                                    action: str, window_seconds: int) -> int:
                                        pass
        return await db.fetchval(
            "SELECT COUNT(*) FROM antinuke_actions WHERE guild_id = ? AND user_id = ? "
            "AND action = ? AND timestamp >= datetime('now', ?)",
            (guild_id, user_id, action, f"-{window_seconds} seconds"),
            default=0,
        )

