from __future__ import annotations
import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.permissions import PermissionManager


class TestPermissions(unittest.TestCase):
    def test_is_guild_owner(self):
        member = MagicMock()
        member.id = 123456789
        member.guild.owner_id = 123456789
        self.assertTrue(PermissionManager.is_guild_owner(member))

        member.id = 987654321
        self.assertFalse(PermissionManager.is_guild_owner(member))

    def test_can_moderate_member_hierarchy(self):
        mod = MagicMock()
        target = MagicMock()
        guild = MagicMock()

        guild.owner_id = 999
        guild.me.top_role.position = 50

        mod.id = 100
        mod.top_role.position = 40

        target.id = 200
        target.top_role.position = 20


        self.assertTrue(PermissionManager.can_moderate_member(mod, target))


        target.top_role.position = 45
        self.assertFalse(PermissionManager.can_moderate_member(mod, target))


        target.id = 999
        self.assertFalse(PermissionManager.can_moderate_member(mod, target))


if __name__ == "__main__":
    unittest.main()

