from __future__ import annotations
import unittest
from workers.onboarding_dispatcher import OnboardingDispatcherWorker


class DummyBot:
    pass


class TestNewWorkers(unittest.TestCase):
    def test_onboarding_dispatcher_queue(self):
        bot = DummyBot()
        worker = OnboardingDispatcherWorker(bot, interval_seconds=30)
        worker.schedule_delayed_role(guild_id=123, user_id=456, role_ids=[789, 101], delay_minutes=5)

        self.assertEqual(len(worker._queue), 1)
        item = worker._queue[0]
        self.assertEqual(item.guild_id, 123)
        self.assertEqual(item.user_id, 456)
        self.assertEqual(item.role_ids, [789, 101])


if __name__ == "__main__":
    unittest.main()
