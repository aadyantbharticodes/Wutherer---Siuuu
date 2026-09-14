from __future__ import annotations
import unittest
from datetime import datetime
from services.onboarding_service import OnboardingService


class DummyMember:
    def __init__(self):
        self.name = "Nova"
        self.id = 555666777
        self.mention = "<@555666777>"
        self.created_at = datetime(2025, 1, 15)
        self.guild = type("Guild", (), {
            "name": "Wutherer Galaxy",
            "id": 123456,
            "member_count": 420,
            "owner": type("Owner", (), {"name": "Admin", "mention": "<@111222>"})()
        })()

    def __str__(self):
        return f"{self.name}#0001"


class TestOnboarding(unittest.TestCase):
    def setUp(self):
        self.member = DummyMember()

    def test_interpolation(self):
        text = "Welcome {user.name} ({user.id}) to {guild.name}! Member #{guild.member_count}. Owned by {owner.name}."
        res = OnboardingService.interpolate(text, self.member)

        self.assertIn("Welcome Nova (555666777)", res)
        self.assertIn("to Wutherer Galaxy!", res)
        self.assertIn("Member #420.", res)
        self.assertIn("Owned by Admin.", res)

    def test_button_builder(self):
        buttons_data = [
            {"label": "Rules", "url": "https://discord.com/rules"},
            {"label": "Website", "url": "https://example.com"}
        ]
        view = OnboardingService.build_buttons(buttons_data)
        self.assertIsNotNone(view)
        self.assertEqual(len(view.children), 2)


if __name__ == "__main__":
    unittest.main()
