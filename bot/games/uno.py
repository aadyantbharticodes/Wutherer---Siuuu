from __future__ import annotations
import random
from typing import Optional, NamedTuple
import discord


class UnoCard(NamedTuple):
    color: str
    value: str

    def __str__(self) -> str:
        color_emojis = {
            "Red": "🟥",
            "Yellow": "🟨",
            "Green": "🟩",
            "Blue": "🟦",
            "Wild": "🌈"
        }
        emoji = color_emojis.get(self.color, "🎴")
        return f"{emoji} {self.color} {self.value}" if self.color != "Wild" else f"{emoji} {self.value}"

    def can_play_on(self, top_card: UnoCard, current_color: Optional[str] = None) -> bool:
        if self.color == "Wild":
            return True
        effective_color = current_color or top_card.color
        if self.color == effective_color:
            return True
        if self.value == top_card.value:
            return True
        return False


UNO_COLORS = ["Red", "Yellow", "Green", "Blue"]
UNO_VALUES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]


class UnoDeck:
    def __init__(self):
        self.cards: list[UnoCard] = []
        for color in UNO_COLORS:
            self.cards.append(UnoCard(color, "0"))
            for val in UNO_VALUES[1:]:
                self.cards.append(UnoCard(color, val))
                self.cards.append(UnoCard(color, val))
        for _ in range(4):
            self.cards.append(UnoCard("Wild", "Wild"))
            self.cards.append(UnoCard("Wild", "+4"))
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> UnoCard:
        if not self.cards:
            self.__init__()
        return self.cards.pop()


class UnoPlayer:
    def __init__(self, user: discord.User | discord.Member):
        self.user = user
        self.hand: list[UnoCard] = []

    @property
    def id(self) -> int:
        return self.user.id

    @property
    def name(self) -> str:
        return self.user.display_name


class UnoGame:
    def __init__(self, players: list[discord.User | discord.Member]):
        self.deck = UnoDeck()
        self.players = [UnoPlayer(p) for p in players]
        self.current_idx = 0
        self.direction = 1
        self.top_card: UnoCard = self.deck.draw()
        while self.top_card.color == "Wild":
            self.top_card = self.deck.draw()
        self.current_color = self.top_card.color
        self.game_over = False
        self.winner: Optional[UnoPlayer] = None

        for p in self.players:
            for _ in range(7):
                p.hand.append(self.deck.draw())

    @property
    def current_player(self) -> UnoPlayer:
        return self.players[self.current_idx]

    def next_turn(self, skip: bool = False) -> None:
        step = 2 if skip else 1
        self.current_idx = (self.current_idx + (self.direction * step)) % len(self.players)

    def play_card(self, player_id: int, card_idx: int, chosen_color: Optional[str] = None) -> tuple[bool, str]:
        if self.game_over:
            return False, "Game is already over."

        if self.current_player.id != player_id:
            return False, "It's not your turn!"

        player = self.current_player
        if not (0 <= card_idx < len(player.hand)):
            return False, "Invalid card selection."

        card = player.hand[card_idx]
        if not card.can_play_on(self.top_card, self.current_color):
            return False, f"You cannot play {card} on top of {self.top_card}!"

        player.hand.pop(card_idx)
        self.top_card = card

        if card.color == "Wild":
            self.current_color = chosen_color or random.choice(UNO_COLORS)
        else:
            self.current_color = card.color

        if len(player.hand) == 0:
            self.game_over = True
            self.winner = player
            return True, f"🎉 {player.name} played their last card and WON the Uno game!"

        msg = f"{player.name} played {card}."
        if card.value == "Reverse":
            if len(self.players) > 2:
                self.direction *= -1
                self.next_turn()
            else:
                self.next_turn(skip=True)
            msg += " Direction reversed!"
        elif card.value == "Skip":
            self.next_turn(skip=True)
            msg += " Next player was skipped!"
        elif card.value == "+2":
            self.next_turn()
            victim = self.current_player
            victim.hand.append(self.deck.draw())
            victim.hand.append(self.deck.draw())
            self.next_turn()
            msg += f" {victim.name} drew 2 cards and was skipped!"
        elif card.value == "+4":
            self.next_turn()
            victim = self.current_player
            for _ in range(4):
                victim.hand.append(self.deck.draw())
            self.next_turn()
            msg += f" {victim.name} drew 4 cards and was skipped!"
        else:
            self.next_turn()

        return True, msg

    def draw_card(self, player_id: int) -> tuple[bool, str]:
        if self.current_player.id != player_id:
            return False, "It's not your turn!"

        card = self.deck.draw()
        self.current_player.hand.append(card)
        self.next_turn()
        return True, f"{self.current_player.name} drew a card from the deck."


class UnoView(discord.ui.View):
    def __init__(self, game: UnoGame):
        super().__init__(timeout=180.0)
        self.game = game
        self._build_controls()

    def _build_controls(self) -> None:
        self.clear_items()
        curr = self.game.current_player

        valid_cards = [
            (idx, c) for idx, c in enumerate(curr.hand)
            if c.can_play_on(self.game.top_card, self.game.current_color)
        ]

        if valid_cards:
            options = []
            for idx, c in valid_cards[:25]:
                options.append(discord.SelectOption(
                    label=str(c)[:100],
                    value=str(idx),
                    description=f"Card #{idx + 1}"
                ))

            select = discord.ui.Select(placeholder="Select a card to play...", options=options)

            async def select_card(interaction: discord.Interaction):
                if interaction.user.id != curr.id:
                    await interaction.response.send_message("It's not your turn!", ephemeral=True)
                    return
                card_idx = int(select.values[0])
                card = curr.hand[card_idx]
                chosen_color = None
                if card.color == "Wild":
                    chosen_color = random.choice(UNO_COLORS)

                ok, msg = self.game.play_card(curr.id, card_idx, chosen_color)
                self._build_controls()
                embed = self.get_embed(status_note=msg)
                await interaction.response.edit_message(embed=embed, view=self)

            select.callback = select_card
            self.add_item(select)

        draw_btn = discord.ui.Button(label="Draw Card", style=discord.ButtonStyle.secondary, emoji="📥")

        async def draw_card_cb(interaction: discord.Interaction):
            if interaction.user.id != curr.id:
                await interaction.response.send_message("It's not your turn!", ephemeral=True)
                return
            ok, msg = self.game.draw_card(curr.id)
            self._build_controls()
            embed = self.get_embed(status_note=msg)
            await interaction.response.edit_message(embed=embed, view=self)

        draw_btn.callback = draw_card_cb
        self.add_item(draw_btn)

    def get_embed(self, status_note: str = "") -> discord.Embed:
        if self.game.game_over:
            title = "🎉 Uno — Game Over!"
            color = 0x57F287
            desc = f"🏆 **{self.game.winner.name}** has won the game!"
        else:
            title = "🎴 Uno Card Showdown"
            color = 0x5865F2
            desc = f"Current Turn: **{self.game.current_player.name}**\nTop Card: **{self.game.top_card}** (Color: **{self.game.current_color}**)"

        if status_note:
            desc += f"\n\n📢 *{status_note}*"

        embed = discord.Embed(title=title, description=desc, color=color)

        scoreboard = []
        for p in self.game.players:
            tag = "👉 " if p.id == self.game.current_player.id and not self.game.game_over else ""
            scoreboard.append(f"{tag}**{p.name}**: {len(p.hand)} cards")
        embed.add_field(name="Players", value="\n".join(scoreboard), inline=False)

        if not self.game.game_over:
            hand_str = " | ".join(f"`{c}`" for c in self.game.current_player.hand[:10])
            if len(self.game.current_player.hand) > 10:
                hand_str += f" *(+{len(self.game.current_player.hand) - 10} more)*"
            embed.add_field(name=f"{self.game.current_player.name}'s Hand", value=hand_str, inline=False)

        embed.set_footer(text="Sentinel Uno Card System")
        return embed
