from __future__ import annotations
import random
from typing import Optional, NamedTuple
import discord


class Card(NamedTuple):
    suit: str
    rank: str
    value: int

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


SUITS = ["♠", "♥", "♦", "♣"]
RANKS = [
    ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6),
    ("7", 7), ("8", 8), ("9", 9), ("10", 10),
    ("J", 10), ("Q", 10), ("K", 10), ("A", 11)
]


class BlackjackDeck:
    def __init__(self, num_decks: int = 1):
        self.cards: list[Card] = []
        for _ in range(num_decks):
            for suit in SUITS:
                for rank, val in RANKS:
                    self.cards.append(Card(suit, rank, val))
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            self.__init__()
        return self.cards.pop()


def calculate_hand(cards: list[Card]) -> int:
    total = sum(c.value for c in cards)
    aces = sum(1 for c in cards if c.rank == "A")
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


class BlackjackGame:
    def __init__(self, bet: int = 50):
        self.bet = bet
        self.deck = BlackjackDeck(2)
        self.player_hand: list[Card] = [self.deck.draw(), self.deck.draw()]
        self.dealer_hand: list[Card] = [self.deck.draw(), self.deck.draw()]
        self.game_over = False
        self.status = "playing"
        self.payout_ratio = 1.0

        if calculate_hand(self.player_hand) == 21:
            if calculate_hand(self.dealer_hand) == 21:
                self.status = "push"
                self.game_over = True
            else:
                self.status = "blackjack"
                self.payout_ratio = 1.5
                self.game_over = True

    def hit(self) -> int:
        if self.game_over:
            return calculate_hand(self.player_hand)
        self.player_hand.append(self.deck.draw())
        total = calculate_hand(self.player_hand)
        if total > 21:
            self.game_over = True
            self.status = "bust"
        elif total == 21:
            self.stand()
        return total

    def double_down(self) -> int:
        if self.game_over or len(self.player_hand) != 2:
            return calculate_hand(self.player_hand)
        self.bet *= 2
        self.player_hand.append(self.deck.draw())
        total = calculate_hand(self.player_hand)
        if total > 21:
            self.game_over = True
            self.status = "bust"
        else:
            self.stand()
        return total

    def stand(self) -> None:
        if self.game_over:
            return
        self.game_over = True
        player_total = calculate_hand(self.player_hand)

        while calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.draw())

        dealer_total = calculate_hand(self.dealer_hand)

        if dealer_total > 21:
            self.status = "dealer_bust"
        elif player_total > dealer_total:
            self.status = "win"
        elif player_total < dealer_total:
            self.status = "lose"
        else:
            self.status = "push"

    def surrender(self) -> None:
        if self.game_over or len(self.player_hand) != 2:
            return
        self.game_over = True
        self.status = "surrender"
        self.bet = self.bet // 2


class BlackjackView(discord.ui.View):
    def __init__(self, author_id: int, bet: int = 50, on_finish=None):
        super().__init__(timeout=120.0)
        self.author_id = author_id
        self.game = BlackjackGame(bet)
        self.on_finish = on_finish
        self._update_buttons()

    def _update_buttons(self) -> None:
        if self.game.game_over:
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True

    def get_embed(self) -> discord.Embed:
        p_cards = "  ".join(f"`{c}`" for c in self.game.player_hand)
        p_score = calculate_hand(self.game.player_hand)

        if self.game.game_over:
            d_cards = "  ".join(f"`{c}`" for c in self.game.dealer_hand)
            d_score = str(calculate_hand(self.game.dealer_hand))
        else:
            d_cards = f"`{self.game.dealer_hand[0]}`  `🂠 ?`"
            d_score = "?"

        status_messages = {
            "playing": ("🃏 Casino Blackjack", 0x5865F2, "Make your move."),
            "blackjack": ("🎉 Natural Blackjack!", 0xFFD700, f"Player hits 21! Payout: 3:2 (+{int(self.game.bet * 1.5)} chips)"),
            "win": ("🏆 Player Wins!", 0x57F287, f"Congratulations! You won +{self.game.bet} chips."),
            "dealer_bust": ("💥 Dealer Busted!", 0x57F287, f"Dealer went over 21. You won +{self.game.bet} chips!"),
            "bust": ("💥 Player Busted!", 0xED4245, f"You exceeded 21. Lost {self.game.bet} chips."),
            "lose": ("💀 Dealer Wins", 0xED4245, f"Dealer beat your hand. Lost {self.game.bet} chips."),
            "push": ("🤝 Push (Tie)", 0xFEE75C, "Hands are tied. Your bet has been refunded."),
            "surrender": ("🏳️ Surrendered", 0x95A5A6, f"You surrendered. Half your bet was returned ({self.game.bet} chips).")
        }

        title, color, desc = status_messages.get(self.game.status, ("Blackjack", 0x5865F2, ""))
        embed = discord.Embed(title=title, description=desc, color=color)
        embed.add_field(name=f"Player's Hand ({p_score})", value=p_cards, inline=False)
        embed.add_field(name=f"Dealer's Hand ({d_score})", value=d_cards, inline=False)
        embed.set_footer(text=f"Current Bet: {self.game.bet} chips")
        return embed

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary, emoji="👉")
    async def hit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        self.game.hit()
        self._update_buttons()
        if self.game.game_over and self.on_finish:
            await self.on_finish(self.game)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.secondary, emoji="🛑")
    async def stand_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        self.game.stand()
        self._update_buttons()
        if self.game.game_over and self.on_finish:
            await self.on_finish(self.game)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Double Down", style=discord.ButtonStyle.success, emoji="💰")
    async def double_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        self.game.double_down()
        self._update_buttons()
        if self.game.game_over and self.on_finish:
            await self.on_finish(self.game)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Surrender", style=discord.ButtonStyle.danger, emoji="🏳️")
    async def surrender_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        self.game.surrender()
        self._update_buttons()
        if self.game.game_over and self.on_finish:
            await self.on_finish(self.game)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
