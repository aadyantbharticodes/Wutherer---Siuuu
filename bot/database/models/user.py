from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.pool import DatabasePool


class UserSettings:
    @staticmethod
    async def get(db: DatabasePool, user_id: int) -> dict:
        row = await db.fetchone("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        if row:
            return row
        return {"user_id": user_id, "noprefix": 0, "badges": "[]"}

    @staticmethod
    async def has_noprefix(db: DatabasePool, user_id: int) -> bool:
        val = await db.fetchval(
            "SELECT noprefix FROM user_settings WHERE user_id = ?", (user_id,)
        )
        return bool(val)

    @staticmethod
    async def set_noprefix(db: DatabasePool, user_id: int, enabled: bool) -> None:
        await db.execute(
            "INSERT INTO user_settings (user_id, noprefix) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET noprefix = ?",
            (user_id, int(enabled), int(enabled)),
        )
        await db.commit()

