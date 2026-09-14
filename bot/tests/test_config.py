import os
import unittest
from unittest.mock import patch
from bot import config


class TestBotConfig(unittest.TestCase):
    def test_default_values(self):
        self.assertEqual(config.DEFAULT_PREFIX, "s!")
        self.assertEqual(config.BOT_COLOR, 0x6C5CE7)
        self.assertEqual(config.BOT_COLOR_SUCCESS, 0x00B894)
        self.assertEqual(config.BOT_COLOR_WARN, 0xFDCB6E)
        self.assertEqual(config.BOT_COLOR_DANGER, 0xD63031)

    def test_database_url_fallback(self):
        self.assertIsNotNone(config.DATABASE_URL)
        self.assertTrue("wutherer.db" in config.DATABASE_URL or "sqlite" in config.DATABASE_URL)

    def test_api_port_type(self):
        self.assertIsInstance(config.API_PORT, int)


if __name__ == "__main__":
    unittest.main()

