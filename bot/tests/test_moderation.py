from __future__ import annotations
import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.checks import can_moderate


class TestModerationChecks(unittest.TestCase):
    def test_can_moderate(self):
        guild = MagicMock()
        guild.owner_id = 1
        guild.me.top_role.position = 100

        target = MagicMock()
        target.id = 2
        target.top_role.position = 10

        mod = MagicMock()
        mod.id = 3
        mod.top_role.position = 20


        self.assertTrue(can_moderate(target, mod, guild))


        target.id = 1
        self.assertFalse(can_moderate(target, mod, guild))


if __name__ == "__main__":
    unittest.main()

