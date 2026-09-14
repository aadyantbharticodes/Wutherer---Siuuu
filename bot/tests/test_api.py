from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.app import create_app


class TestAPIApp(unittest.TestCase):
    def test_create_app(self):
        app = create_app(bot=None)
        self.assertIsNotNone(app)
        self.assertEqual(app.title, "Sentinel Control Panel API")

        routes = [r.path for r in app.routes]
        self.assertIn("/api/health", routes)
        self.assertIn("/api/bot/stats", routes)


if __name__ == "__main__":
    unittest.main()

