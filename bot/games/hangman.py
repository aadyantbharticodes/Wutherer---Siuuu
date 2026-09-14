from __future__ import annotations
import random
from typing import Optional
import discord

HANGMAN_PICS = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
========="""
]

WORD_CATEGORIES = {
    "Gaming": [
        "MINECRAFT", "VALORANT", "OVERWATCH", "CYBERPUNK", "FORTNITE",
        "TERRARIA", "ELDENRING", "BLOODBORNE", "DARKSOULS", "WITCHER",
        "WARFRAME", "RUNESCAPE", "POKEMON", "ASSASSIN", "BIOSHOCK"
    ],
    "Programming": [
        "PYTHON", "TYPESCRIPT", "JAVASCRIPT", "DATABASE", "CONTAINER",
        "KUBERNETES", "ALGORITHM", "RECURSION", "FRAMEWORK", "COMPILER",
        "BYTECODE", "COROUTINE", "DECORATOR", "POLYMORPHISM", "MUTEX"
    ],
    "Science": [
        "GRAVITATION", "PHOTOSYNTHESIS", "ASTRONOMY", "QUANTUM", "MOLECULE",
        "ELECTROMAGNETISM", "SUPERNOVA", "CHROMOSOME", "THERMODYNAMICS",
        "NEUROSCIENCE", "MITOCHONDRIA", "EXOPLANET", "SEISMOLOGY"
    ],
    "Countries": [
        "ARGENTINA", "AUSTRALIA", "SINGAPORE", "SWITZERLAND", "NETHERLANDS",
        "PORTUGAL", "MADAGASCAR", "INDONESIA", "PHILIPPINES", "NORWAY",
        "DENMARK", "BRAZIL", "COLOMBIA", "GERMANY", "THAILAND"
    ],
    "Anime": [
        "EVANGELION", "BERSERK", "FULLMETAL", "NARUTO", "ONEPIECE",
        "BLEACH", "DEATHNOTE", "STEINSGATE", "VINLAND", "CHAINSAW"
    ]
}


class HangmanGame:
    def __init__(self, category: Optional[str] = None):
        if category and category in WORD_CATEGORIES:
            self.category = category
        else:
            self.category = random.choice(list(WORD_CATEGORIES.keys()))

        self.word = random.choice(WORD_CATEGORIES[self.category])
        self.guessed_letters: set[str] = set()
        self.mistakes = 0
        self.max_mistakes = len(HANGMAN_PICS) - 1
        self.game_over = False
        self.won = False

    def guess(self, letter: str) -> bool:
        if self.game_over:
            return False

        letter = letter.upper()
        if len(letter) != 1 or not letter.isalpha():
            return False

        if letter in self.guessed_letters:
            return False

        self.guessed_letters.add(letter)

        if letter not in self.word:
            self.mistakes += 1
            if self.mistakes >= self.max_mistakes:
                self.game_over = True
                self.won = False
                return True
        else:
            if all(ch in self.guessed_letters for ch in self.word):
                self.won = True
                self.game_over = True
                return True

        return True

    def get_display_word(self) -> str:
        return " ".join(ch if ch in self.guessed_letters else "_" for ch in self.word)

    def get_ascii_gallows(self) -> str:
        idx = min(self.mistakes, self.max_mistakes)
        return HANGMAN_PICS[idx]


class HangmanView(discord.ui.View):
    def __init__(self, author_id: int, category: Optional[str] = None):
        super().__init__(timeout=180.0)
        self.author_id = author_id
        self.game = HangmanGame(category)

    def get_embed(self) -> discord.Embed:
        if self.game.won:
            title = "🎉 Hangman — Victory!"
            color = 0x57F287
            status = f"Awesome job! The word was **{self.game.word}**."
        elif self.game.game_over:
            title = "💀 Hangman — Game Over!"
            color = 0xED4245
            status = f"Out of guesses! The word was **{self.game.word}**."
        else:
            title = "🪢 Hangman"
            color = 0x5865F2
            status = "Type a single letter in chat to guess!"

        gallows = f"```\n{self.game.get_ascii_gallows()}\n```"
        display = f"### `{self.game.get_display_word()}`"
        guessed = ", ".join(sorted(self.game.guessed_letters)) if self.game.guessed_letters else "*None*"

        embed = discord.Embed(title=title, color=color)
        embed.description = f"{status}\n{gallows}\n{display}"
        embed.add_field(name="Category", value=f"📚 **{self.game.category}**", inline=True)
        embed.add_field(name="Remaining Tries", value=f"❤️ **{self.game.max_mistakes - self.game.mistakes}**", inline=True)
        embed.add_field(name="Guessed Letters", value=f"`{guessed}`", inline=False)
        embed.set_footer(text="Type letters in this channel to guess • Sentinel Games")
        return embed

    @discord.ui.button(label="Surrender / Reveal", style=discord.ButtonStyle.danger, emoji="🏳️")
    async def surrender_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        self.game.game_over = True
        self.game.won = False
        button.disabled = True
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
