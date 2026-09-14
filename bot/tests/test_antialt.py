from __future__ import annotations
import unittest
from games.slots import SlotMachine


class TestSlotsAndAntiAlt(unittest.TestCase):
    def test_slots_spin(self):
        result, payout = SlotMachine.spin(100)
        self.assertEqual(len(result.reels), 3)
        self.assertIsInstance(result.multiplier, float)
        self.assertIsInstance(payout, int)
        if result.is_jackpot:
            self.assertEqual(result.reels[0], "7️⃣")
            self.assertEqual(payout, 2500)


if __name__ == "__main__":
    unittest.main()
