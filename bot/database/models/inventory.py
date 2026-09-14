from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, List, Optional
import aiosqlite


@dataclass
class InventoryItem:
    entry_id: int
    guild_id: int
    user_id: int
    item_id: int
    item_name: str
    item_type: str
    quantity: int = 1
    acquired_at: int = field(default_factory=lambda: int(time.time()))


class InventoryModel:

    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def add_item(
        self,
        guild_id: int,
        user_id: int,
        item_id: int,
        item_name: str,
        item_type: str,
        quantity: int = 1,
    ) -> None:
        query = """
            INSERT INTO user_inventory (guild_id, user_id, item_id, item_name, item_type, quantity, acquired_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(guild_id, user_id, item_id) DO UPDATE SET
                quantity = user_inventory.quantity + excluded.quantity
        """
        now = int(time.time())
        await self.db.execute(
            query,
            (guild_id, user_id, item_id, item_name, item_type, quantity, now),
        )
        await self.db.commit()

    async def remove_item(
        self,
        guild_id: int,
        user_id: int,
        item_id: int,
        quantity: int = 1,
    ) -> bool:
        query_check = "SELECT quantity FROM user_inventory WHERE guild_id = ? AND user_id = ? AND item_id = ?"
        async with self.db.execute(query_check, (guild_id, user_id, item_id)) as cursor:
            row = await cursor.fetchone()
            if not row or row[0] < quantity:
                return False
            current_qty = row[0]

        if current_qty == quantity:
            query_del = "DELETE FROM user_inventory WHERE guild_id = ? AND user_id = ? AND item_id = ?"
            await self.db.execute(query_del, (guild_id, user_id, item_id))
        else:
            query_dec = "UPDATE user_inventory SET quantity = quantity - ? WHERE guild_id = ? AND user_id = ? AND item_id = ?"
            await self.db.execute(query_dec, (quantity, guild_id, user_id, item_id))

        await self.db.commit()
        return True

    async def get_user_inventory(self, guild_id: int, user_id: int) -> List[InventoryItem]:
        query = """
            SELECT entry_id, guild_id, user_id, item_id, item_name, item_type, quantity, acquired_at
            FROM user_inventory
            WHERE guild_id = ? AND user_id = ? AND quantity > 0
            ORDER BY acquired_at DESC
        """
        async with self.db.execute(query, (guild_id, user_id)) as cursor:
            rows = await cursor.fetchall()
            return [
                InventoryItem(
                    entry_id=r[0],
                    guild_id=r[1],
                    user_id=r[2],
                    item_id=r[3],
                    item_name=r[4],
                    item_type=r[5],
                    quantity=r[6],
                    acquired_at=r[7],
                )
                for r in rows
            ]

    async def transfer_item(
        self,
        guild_id: int,
        sender_id: int,
        recipient_id: int,
        item_id: int,
        item_name: str,
        item_type: str,
        quantity: int = 1,
    ) -> bool:
        success = await self.remove_item(guild_id, sender_id, item_id, quantity)
        if not success:
            return False
        await self.add_item(guild_id, recipient_id, item_id, item_name, item_type, quantity)
        return True

