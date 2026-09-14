from __future__ import annotations
import unittest
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.models.leveling import UserLevels


class TestDatabaseModels(unittest.IsolatedAsyncioTestCase):
    def test_level_calculations(self):

        xp_lvl_1 = UserLevels.xp_for_level(1)
        self.assertEqual(xp_lvl_1, 100)

        xp_lvl_5 = UserLevels.xp_for_level(5)
        self.assertEqual(xp_lvl_5, 500)


        self.assertEqual(UserLevels.level_for_xp(99), 0)
        self.assertEqual(UserLevels.level_for_xp(100), 1)
        self.assertEqual(UserLevels.level_for_xp(550), 5)


if __name__ == "__main__":
    unittest.main()

