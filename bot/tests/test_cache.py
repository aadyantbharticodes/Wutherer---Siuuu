from __future__ import annotations
import unittest
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.cache import TTLCache


class TestTTLCache(unittest.TestCase):
    def test_cache_set_and_get(self):
        cache = TTLCache(default_ttl=60)
        cache.set("foo", "bar")
        self.assertEqual(cache.get("foo"), "bar")

    def test_cache_expiry(self):
        cache = TTLCache(default_ttl=0.1)
        cache.set("key", "val")
        self.assertEqual(cache.get("key"), "val")
        time.sleep(0.15)
        self.assertIsNone(cache.get("key"))

    def test_cache_delete(self):
        cache = TTLCache()
        cache.set("temp", 123)
        cache.delete("temp")
        self.assertIsNone(cache.get("temp"))


if __name__ == "__main__":
    unittest.main()

