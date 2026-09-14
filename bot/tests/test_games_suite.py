from __future__ import annotations
import unittest
from games.minesweeper import MinesweeperGame
from games.blackjack import BlackjackGame, calculate_hand, Card, BlackjackDeck
from games.hangman import HangmanGame, WORD_CATEGORIES
from games.trivia import TRIVIA_BANK


class TestGamesSuite(unittest.TestCase):
    def test_minesweeper_init(self):
        game = MinesweeperGame(size=5, bombs=4)
        self.assertEqual(game.size, 5)
        self.assertEqual(game.bombs, 4)
        self.assertFalse(game.game_over)
        self.assertFalse(game.won)

        bomb_count = sum(row.count(-1) for row in game.grid)
        self.assertEqual(bomb_count, 4)

    def test_minesweeper_flag_toggle(self):
        game = MinesweeperGame(size=4, bombs=2)
        game.flag_mode = True
        game.click_cell(0, 0)
        self.assertTrue(game.flagged[0][0])
        game.click_cell(0, 0)
        self.assertFalse(game.flagged[0][0])

    def test_blackjack_hand_calculation(self):
        hand1 = [Card("♠", "10", 10), Card("♦", "K", 10)]
        self.assertEqual(calculate_hand(hand1), 20)

        hand2 = [Card("♠", "A", 11), Card("♦", "9", 9)]
        self.assertEqual(calculate_hand(hand2), 20)

        hand3 = [Card("♠", "A", 11), Card("♦", "9", 9), Card("♣", "5", 5)]
        self.assertEqual(calculate_hand(hand3), 15)

        hand4 = [Card("♠", "A", 11), Card("♦", "A", 11)]
        self.assertEqual(calculate_hand(hand4), 12)

    def test_blackjack_game_mechanics(self):
        game = BlackjackGame(bet=100)
        self.assertEqual(game.bet, 100)
        self.assertEqual(len(game.player_hand), 2)
        self.assertEqual(len(game.dealer_hand), 2)

        if not game.game_over:
            game.stand()
            self.assertTrue(game.game_over)
            self.assertIn(game.status, ("win", "lose", "push", "dealer_bust"))

    def test_hangman_word_selection(self):
        game = HangmanGame(category="Gaming")
        self.assertEqual(game.category, "Gaming")
        self.assertIn(game.word, WORD_CATEGORIES["Gaming"])

        first_letter = game.word[0]
        game.guess(first_letter)
        self.assertIn(first_letter, game.guessed_letters)

        game.guess("Z" if "Z" not in game.word else "Q")
        self.assertTrue(game.mistakes > 0 or "Z" in game.word)

    def test_trivia_questions_integrity(self):
        self.assertTrue(len(TRIVIA_BANK) >= 20)
        for q in TRIVIA_BANK:
            self.assertEqual(len(q.options), 4)
            self.assertTrue(0 <= q.correct_index < 4)
            self.assertTrue(len(q.question) > 5)
            self.assertTrue(len(q.explanation) > 0)


if __name__ == "__main__":
    unittest.main()
