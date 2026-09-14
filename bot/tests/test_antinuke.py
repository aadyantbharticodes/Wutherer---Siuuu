from __future__ import annotations
import unittest
import time
from services.antinuke import AntiNukeService


class DummyDB:
    pass


class DummyBot:
    def __init__(self):
        self.user = type("User", (), {"id": 999999})()


class TestAntiNuke(unittest.TestCase):
    def setUp(self):
        self.bot = DummyBot()
        self.db = DummyDB()
        self.service = AntiNukeService(self.bot, self.db)

    def test_record_action_window(self):
        guild_id = 12345
        user_id = 67890
        action = "channel_delete"

        count1 = self.service.record_action(guild_id, user_id, action, window_seconds=10)
        self.assertEqual(count1, 1)

        count2 = self.service.record_action(guild_id, user_id, action, window_seconds=10)
        self.assertEqual(count2, 2)

        count3 = self.service.record_action(guild_id, user_id, action, window_seconds=10)
        self.assertEqual(count3, 3)

    def test_separate_buckets_per_user_and_action(self):
        guild_id = 12345
        user_a = 111
        user_b = 222

        self.service.record_action(guild_id, user_a, "channel_delete", 15)
        self.service.record_action(guild_id, user_a, "channel_delete", 15)
        count_b = self.service.record_action(guild_id, user_b, "channel_delete", 15)

        self.assertEqual(count_b, 1)

        count_role = self.service.record_action(guild_id, user_a, "role_delete", 15)
        self.assertEqual(count_role, 1)


if __name__ == "__main__":
    unittest.main()
