import unittest
from PIL import Image
from bot.services.welcome_card import WelcomeCardGenerator


class TestWelcomeCardGenerator(unittest.TestCase):
    def test_create_card_dimensions_and_format(self):
        buf = WelcomeCardGenerator.create_card(
            member_name="Aadyant",
            guild_name="Wutherer Core",
            member_count=1337,
            avatar_bytes=None,
        )
        self.assertIsNotNone(buf)
        img = Image.open(buf)
        self.assertEqual(img.size, (1024, 450))
        self.assertEqual(img.format, "PNG")


if __name__ == "__main__":
    unittest.main()

