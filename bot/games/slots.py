from __future__ import annotations
import random
from typing import NamedTuple

SLOT_SYMBOLS = [
    ("🍒", 2.0, "Cherries"),
    ("🍋", 3.0, "Lemons"),
    ("🍇", 5.0, "Grapes"),
    ("🔔", 10.0, "Bells"),
    ("💎", 15.0, "Diamonds"),
    ("7️⃣", 25.0, "Lucky Sevens"),
]

WEIGHTS = [35, 25, 18, 12, 7, 3]


class SpinResult(NamedTuple):
    reels: list[str]
    multiplier: float
    is_jackpot: bool
    description: str


class SlotMachine:
    @staticmethod
    def spin(bet: int) -> tuple[SpinResult, int]:
        symbols = [s[0] for s in SLOT_SYMBOLS]
        reels = random.choices(symbols, weights=WEIGHTS, k=3)

        if reels[0] == reels[1] == reels[2]:
            symbol = reels[0]
            mult = next(s[1] for s in SLOT_SYMBOLS if s[0] == symbol)
            is_jackpot = (symbol == "7️⃣")
            payout = int(bet * mult)
            desc = f"JACKPOT! Triple {symbol} pays {mult}x!" if is_jackpot else f"Triple {symbol}! Won {mult}x your bet!"
            return SpinResult(reels, mult, is_jackpot, desc), payout
        elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
            mult = 1.5
            payout = int(bet * mult)
            desc = "Pair match! Won 1.5x your bet."
            return SpinResult(reels, mult, False, desc), payout
        else:
            return SpinResult(reels, 0.0, False, "No matching symbols. Better luck next spin!"), 0
