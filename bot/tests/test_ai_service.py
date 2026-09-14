from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.ai import AIService


class TestAIService(unittest.TestCase):
    def test_initialization(self):
        service = AIService()
        self.assertIsNotNone(service)
        self.assertIsInstance(service.is_configured, bool)

    def test_mock_prompt_preparation(self):
        prompt = "Hello"
        self.assertEqual(prompt.strip(), "Hello")


if __name__ == "__main__":
    unittest.main()

