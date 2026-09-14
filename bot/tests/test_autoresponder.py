import re
import unittest
from bot.database.models.autoresponder import AutoResponseTrigger


class TestAutoResponder(unittest.TestCase):
    def setUp(self):
        self.trigger_exact = AutoResponseTrigger(
            trigger_id=1,
            guild_id=123,
            trigger_text="hello",
            response_text="world",
            match_mode="exact",
        )
        self.trigger_wildcard = AutoResponseTrigger(
            trigger_id=2,
            guild_id=123,
            trigger_text="ping",
            response_text="pong",
            match_mode="wildcard",
        )

    def test_matching_logic(self):

        msg1 = "hello"
        self.assertEqual(msg1.lower(), self.trigger_exact.trigger_text.lower())

        msg2 = "hello there"
        self.assertNotEqual(msg2.lower(), self.trigger_exact.trigger_text.lower())


        self.assertTrue(self.trigger_wildcard.trigger_text.lower() in "a big ping test".lower())
        self.assertFalse(self.trigger_wildcard.trigger_text.lower() in "something else".lower())


if __name__ == "__main__":
    unittest.main()

