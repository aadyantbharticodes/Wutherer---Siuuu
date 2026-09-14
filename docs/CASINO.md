# Casino & Interactive Games Suite

Wutherer provides a collection of interactive Discord games and casino mini-games integrated directly with the server economy and wallet chip balances.

---

## Games

### 1. Casino Blackjack (`s!blackjack <bet>`)
- **Deck Engine**: Standard 52-card shoe (2 decks shuffled continuously).
- **Ace Handling**: Dynamically computes soft vs. hard Ace values (1 vs. 11).
- **Dealer AI**: Dealer draws cards until reaching soft 17 or higher.
- **Interactive UI**: Discord Action Buttons (`Hit`, `Stand`, `Double Down`, `Surrender`).
- **Payout Table**:
  - Natural Blackjack (Ace + 10-value card): **3:2** payout.
  - Standard Victory: **1:1** payout.
  - Dealer Bust: **1:1** payout.
  - Push (Tie): **100%** bet refunded.
  - Surrender: **50%** bet refunded.

### 2. Casino Slot Machine (`s!slots <bet>`)
- **Animated Reels**: 3 spinning reels with weighted symbols:
  - 🍒 Cherries: **2x** multiplier
  - 🍋 Lemons: **3x** multiplier
  - 🍇 Grapes: **5x** multiplier
  - 🔔 Bells: **10x** multiplier
  - 💎 Diamonds: **15x** multiplier
  - 7️⃣ Lucky Sevens: **25x** Jackpot multiplier
  - Any Pair Match: **1.5x** multiplier

### 3. Minesweeper (`s!minesweeper [easy/medium/hard]`)
- **Grid Generator**: Button-based minefield (`4x4` easy, `5x5` medium, `5x6` hard).
- **Interactive Controls**:
  - Click cells to reveal adjacent mine count.
  - Recursive flood-fill expansion for 0-bomb safe zones.
  - Toggle **Flag Mode** button to mark suspected bomb locations.

### 4. Multiplayer Uno Showdown (`s!uno <@opponent>`)
- **Full 108 Card Deck**:
  - 4 Colors: Red, Yellow, Green, Blue
  - Values: 0–9, Skip, Reverse, Draw 2 (+2)
  - Special Wilds: Wild Color Pick, Wild Draw 4 (+4)
- **Turn Engine**: Dynamic turn order, reverse direction, card penalty skips, and interactive select dropdowns to play valid cards.

### 5. Hangman (`s!hangman [category]`)
- **Visual Gallows**: 8 stages of ASCII gallows drawings.
- **Categories**: Gaming, Programming, Science, Countries, Anime.
- **Gameplay**: Real-time channel chat letter listener with remaining attempts tracking.

### 6. Trivia Engine (`s!trivia [category]`)
- **Question Bank**: 100+ curated multiple-choice questions across Science, Technology, Gaming, Geography, and History.
- **Interactive Buttons**: Instant answer verification and detailed explanations.
