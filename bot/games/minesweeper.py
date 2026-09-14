from __future__ import annotations
import random
from typing import Optional, Union
import discord


class MinesweeperGame:
    def __init__(self, size: int = 5, bombs: int = 4):
        self.size = min(max(size, 4), 5)
        self.bombs = min(bombs, (self.size * self.size) - 2)
        self.grid: list[list[int]] = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.revealed: list[list[bool]] = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.flagged: list[list[bool]] = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.game_over = False
        self.won = False
        self.flag_mode = False
        self._init_bombs()

    def _init_bombs(self) -> None:
        placed = 0
        while placed < self.bombs:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            if self.grid[r][c] != -1:
                self.grid[r][c] = -1
                placed += 1

        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == -1:
                    continue
                self.grid[r][c] = self._count_adjacent_bombs(r, c)

    def _count_adjacent_bombs(self, r: int, c: int) -> int:
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if self.grid[nr][nc] == -1:
                        count += 1
        return count

    def click_cell(self, r: int, c: int) -> bool:
        if self.game_over:
            return False

        if self.flag_mode:
            self.flagged[r][c] = not self.flagged[r][c]
            return True

        if self.flagged[r][c]:
            return True

        if self.grid[r][c] == -1:
            self.game_over = True
            self.won = False
            self._reveal_all()
            return True

        self._flood_reveal(r, c)
        self._check_win()
        return True

    def _flood_reveal(self, r: int, c: int) -> None:
        if not (0 <= r < self.size and 0 <= nc < self.size if 'nc' in locals() else 0 <= c < self.size):
            return
        if self.revealed[r][c] or self.flagged[r][c]:
            return

        self.revealed[r][c] = True

        if self.grid[r][c] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if not self.revealed[nr][nc]:
                            self._flood_reveal(nr, nc)

    def _reveal_all(self) -> None:
        for r in range(self.size):
            for c in range(self.size):
                self.revealed[r][c] = True

    def _check_win(self) -> None:
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != -1 and not self.revealed[r][c]:
                    return
        self.won = True
        self.game_over = True
        self._reveal_all()


class MinesweeperButton(discord.ui.Button["MinesweeperView"]):
    def __init__(self, r: int, c: int):
        self.r = r
        self.c = c
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=r)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view = self.view
        if interaction.user.id != view.author_id:
            await interaction.response.send_message("This is not your Minesweeper game!", ephemeral=True)
            return

        view.game.click_cell(self.r, self.c)
        view.update_buttons()

        embed = view.get_embed()
        await interaction.response.edit_message(embed=embed, view=view)


class MinesweeperView(discord.ui.View):
    def __init__(self, author_id: int, size: int = 5, bombs: int = 4):
        super().__init__(timeout=180.0)
        self.author_id = author_id
        self.game = MinesweeperGame(size, bombs)
        self._build_grid()

    def _build_grid(self) -> None:
        self.clear_items()
        for r in range(self.game.size):
            for c in range(self.game.size):
                self.add_item(MinesweeperButton(r, c))

        mode_btn = discord.ui.Button(
            label="Flag Mode: OFF" if not self.game.flag_mode else "Flag Mode: ON 🚩",
            style=discord.ButtonStyle.primary if not self.game.flag_mode else discord.ButtonStyle.danger,
            row=self.game.size
        )

        async def toggle_flag(interaction: discord.Interaction):
            if interaction.user.id != self.author_id:
                await interaction.response.send_message("This is not your game!", ephemeral=True)
                return
            self.game.flag_mode = not self.game.flag_mode
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_embed(), view=self)

        mode_btn.callback = toggle_flag
        self.add_item(mode_btn)
        self.update_buttons()

    def update_buttons(self) -> None:
        emoji_map = {
            0: "⬜", 1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣",
            5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", -1: "💥"
        }

        for item in self.children:
            if isinstance(item, MinesweeperButton):
                r, c = item.r, item.c
                if self.game.revealed[r][c]:
                    val = self.game.grid[r][c]
                    item.label = None
                    item.emoji = emoji_map.get(val, "⬜")
                    item.style = discord.ButtonStyle.danger if val == -1 else discord.ButtonStyle.success if val == 0 else discord.ButtonStyle.primary
                    item.disabled = True
                elif self.game.flagged[r][c]:
                    item.label = None
                    item.emoji = "🚩"
                    item.style = discord.ButtonStyle.danger
                    item.disabled = self.game.game_over
                else:
                    item.label = "\u200b"
                    item.emoji = None
                    item.style = discord.ButtonStyle.secondary
                    item.disabled = self.game.game_over
            elif isinstance(item, discord.ui.Button) and item.row == self.game.size:
                item.label = "Flag Mode: OFF" if not self.game.flag_mode else "Flag Mode: ON 🚩"
                item.style = discord.ButtonStyle.primary if not self.game.flag_mode else discord.ButtonStyle.danger
                item.disabled = self.game.game_over

    def get_embed(self) -> discord.Embed:
        if self.game.won:
            title = "🏆 Minesweeper — Victory!"
            color = 0x57F287
            desc = "Congratulations! You successfully cleared the entire minefield."
        elif self.game.game_over:
            title = "💥 Minesweeper — Game Over!"
            color = 0xED4245
            desc = "Boom! You hit a hidden landmine."
        else:
            title = "💣 Minesweeper"
            color = 0x5865F2
            desc = f"Grid: **{self.game.size}x{self.game.size}** | Hidden Bombs: **{self.game.bombs}**\nClick a tile to reveal it or toggle **Flag Mode** to mark bombs."

        embed = discord.Embed(title=title, description=desc, color=color)
        embed.set_footer(text="Sentinel Interactive Games")
        return embed
