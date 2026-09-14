from __future__ import annotations
import unittest
from games.uno import UnoGame, UnoCard, UnoDeck


class DummyUser:
    def __init__(self, uid: int, name: str):
        self.id = uid
        self.display_name = name


class TestUno(unittest.TestCase):
    def test_deck_composition(self):
        deck = UnoDeck()
        self.assertEqual(len(deck.cards), 108)

    def test_card_matching(self):
        c1 = UnoCard("Red", "5")
        c2 = UnoCard("Red", "7")
        c3 = UnoCard("Blue", "5")
        c4 = UnoCard("Green", "2")
        wild = UnoCard("Wild", "Wild")

        self.assertTrue(c2.can_play_on(c1))
        self.assertTrue(c3.can_play_on(c1))
        self.assertFalse(c4.can_play_on(c1))
        self.assertTrue(wild.can_play_on(c1))

    def test_game_init(self):
        p1 = DummyUser(101, "Alice")
        p2 = DummyUser(102, "Bob")
        game = UnoGame([p1, p2])

        self.assertEqual(len(game.players), 2)
        self.assertEqual(len(game.players[0].hand), 7)
        self.assertEqual(len(game.players[1].hand), 7)
        self.assertIn(game.top_card.color, ("Red", "Yellow", "Green", "Blue"))
        self.assertFalse(game.game_over)


if __name__ == "__main__":
    unittest.main()
