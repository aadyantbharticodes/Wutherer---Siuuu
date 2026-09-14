import unittest
from bot.database.models.shop import ShopItem
from bot.database.models.inventory import InventoryItem


class TestShopAndInventoryModels(unittest.TestCase):
    def test_shop_item_creation(self):
        item = ShopItem(
            item_id=1,
            guild_id=123,
            name="VIP Role",
            description="Grants exclusive channel perks",
            price=2500,
            item_type="role",
            role_id=999888,
        )
        self.assertEqual(item.price, 2500)
        self.assertEqual(item.item_type, "role")
        self.assertEqual(item.role_id, 999888)

    def test_inventory_item_creation(self):
        inv = InventoryItem(
            entry_id=1,
            guild_id=123,
            user_id=456,
            item_id=1,
            item_name="VIP Role",
            item_type="role",
            quantity=1,
        )
        self.assertEqual(inv.quantity, 1)
        self.assertEqual(inv.user_id, 456)


if __name__ == "__main__":
    unittest.main()

