import unittest
from unittest.mock import MagicMock
from bot.workers.analytics_aggregator import AnalyticsAggregatorWorker
from bot.workers.giveaway_checker import GiveawayCheckerWorker
from bot.workers.mc_status_updater import MinecraftStatusUpdaterWorker
from bot.workers.reminder_dispatcher import ReminderDispatcherWorker
from bot.workers.youtube_monitor import YouTubeMonitorWorker


class TestBackgroundWorkers(unittest.TestCase):
    def setUp(self):
        self.mock_bot = MagicMock()
        self.mock_bot.db_pool = MagicMock()
        self.mock_bot.guilds = []

    def test_analytics_worker_init(self):
        worker = AnalyticsAggregatorWorker(self.mock_bot, interval_seconds=120)
        self.assertEqual(worker.interval, 120)
        self.assertFalse(worker._running)

    def test_giveaway_worker_init(self):
        worker = GiveawayCheckerWorker(self.mock_bot)
        self.assertIsNotNone(worker)

    def test_mc_worker_init(self):
        worker = MinecraftStatusUpdaterWorker(self.mock_bot)
        self.assertIsNotNone(worker)

    def test_reminder_worker_init(self):
        worker = ReminderDispatcherWorker(self.mock_bot)
        self.assertIsNotNone(worker)

    def test_youtube_worker_init(self):
        worker = YouTubeMonitorWorker(self.mock_bot)
        self.assertIsNotNone(worker)


if __name__ == "__main__":
    unittest.main()

