from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, List, Optional
import aiosqlite


@dataclass
class ShopItem:
    item_id: int
    guild_id: int
    name: str
    description: str
    price: int
    item_type: str = "role"
    role_id: Optional[int] = None
    stock: int = -1
    enabled: bool = True
    created_at: int = field(default_factory=lambda: int(time.time()))


class ShopModel:

    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def add_item(
        self,
        guild_id: int,
        name: str,
        description: str,
        price: int,
        item_type: str = "role",
        role_id: Optional[int] = None,
        stock: int = -1,
    ) -> int:
        query = """
            INSERT INTO shop_items (
                guild_id, name, description, price, item_type, role_id, stock, enabled, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
        """
        now = int(time.time())
        cursor = await self.db.execute(
            query,
            (guild_id, name, description, price, item_type, role_id, stock, now),
        )
        await self.db.commit()
        return cursor.lastrowid

    async def get_item(self, item_id: int, guild_id: int) -> Optional[ShopItem]:
        query = "SELECT * FROM shop_items WHERE item_id = ? AND guild_id = ?"
        async with self.db.execute(query, (item_id, guild_id)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            return self._row_to_item(row)

    async def list_items(self, guild_id: int, include_disabled: bool = False) -> List[ShopItem]:
        if include_disabled:
            query = "SELECT * FROM shop_items WHERE guild_id = ? ORDER BY price ASC"
            params = (guild_id,)
        else:
            query = "SELECT * FROM shop_items WHERE guild_id = ? AND enabled = 1 ORDER BY price ASC"
            params = (guild_id,)

        async with self.db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [self._row_to_item(r) for r in rows]

    async def delete_item(self, item_id: int, guild_id: int) -> bool:
        query = "DELETE FROM shop_items WHERE item_id = ? AND guild_id = ?"
        cursor = await self.db.execute(query, (item_id, guild_id))
        await self.db.commit()
        return cursor.rowcount > 0

    async def decrement_stock(self, item_id: int) -> bool:
        query = "UPDATE shop_items SET stock = stock - 1 WHERE item_id = ? AND stock > 0"
        cursor = await self.db.execute(query, (item_id,))
        await self.db.commit()
        return cursor.rowcount > 0

    def _row_to_item(self, row: Any) -> ShopItem:
        return ShopItem(
            item_id=row[0],
            guild_id=row[1],
            name=row[2],
            description=row[3],
            price=row[4],
            item_type=row[5],
            role_id=row[6],
            stock=row[7],
            enabled=bool(row[8]),
            created_at=row[9],
        )

