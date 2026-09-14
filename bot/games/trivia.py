from __future__ import annotations
import random
from typing import Optional, NamedTuple
import discord


class TriviaQuestion(NamedTuple):
    category: str
    question: str
    options: list[str]
    correct_index: int
    explanation: str


TRIVIA_BANK: list[TriviaQuestion] = [
    TriviaQuestion("Science", "What is the most abundant gas in Earth's atmosphere?", ["Oxygen", "Nitrogen", "Argon", "Carbon Dioxide"], 1, "Nitrogen makes up approximately 78% of Earth's atmosphere."),
    TriviaQuestion("Science", "What is the chemical symbol for Tungsten?", ["Tu", "Tg", "W", "Tn"], 2, "Tungsten's symbol W comes from its former name Wolfram."),
    TriviaQuestion("Science", "What particle carries a positive electric charge?", ["Electron", "Neutron", "Positron", "Proton"], 3, "Protons carry a positive charge of +1e inside atomic nuclei."),
    TriviaQuestion("Science", "How many bones are in the adult human body?", ["186", "206", "216", "226"], 1, "An adult human skeleton has 206 bones."),
    TriviaQuestion("Science", "What is the closest planet to the Sun?", ["Venus", "Mercury", "Mars", "Earth"], 1, "Mercury orbits closest to the Sun at an average distance of 57.9 million km."),

    TriviaQuestion("Technology", "In what year was the Python programming language first released?", ["1989", "1991", "1995", "2000"], 1, "Guido van Rossum released Python 0.9.0 in February 1991."),
    TriviaQuestion("Technology", "What does 'HTTP' stand for?", ["HyperText Transfer Protocol", "HighTech Transmission Process", "Hyperlink Text Transmission Path", "HyperText Terminal Protocol"], 0, "HTTP stands for HyperText Transfer Protocol."),
    TriviaQuestion("Technology", "Who created the Linux kernel?", ["Richard Stallman", "Linus Torvalds", "Ken Thompson", "Dennis Ritchie"], 1, "Linus Torvalds created Linux in 1991 at the University of Helsinki."),
    TriviaQuestion("Technology", "What is the standard port used for secure HTTPS traffic?", ["80", "443", "8080", "22"], 1, "HTTPS runs over TLS/SSL on port 443 by default."),
    TriviaQuestion("Technology", "Which data structure operates on a 'First-In, First-Out' (FIFO) basis?", ["Stack", "Queue", "Heap", "Hash Map"], 1, "Queues operate strictly on a FIFO principle."),

    TriviaQuestion("Gaming", "What was the highest-selling video game console of all time?", ["Nintendo Switch", "PlayStation 2", "PlayStation 4", "Xbox 360"], 1, "The PlayStation 2 has sold over 155 million units worldwide."),
    TriviaQuestion("Gaming", "In 'The Legend of Zelda', what is the name of the protagonist?", ["Zelda", "Ganon", "Link", "Epona"], 2, "Link is the heroic protagonist, while Zelda is the Princess."),
    TriviaQuestion("Gaming", "Which developer created the original 'Dark Souls' game?", ["Capcom", "FromSoftware", "Bethesda", "Square Enix"], 1, "FromSoftware and director Hidetaka Miyazaki created Dark Souls."),
    TriviaQuestion("Gaming", "What year was Minecraft first released in public alpha?", ["2008", "2009", "2010", "2011"], 1, "Markus Persson released the initial Minecraft alpha in May 2009."),
    TriviaQuestion("Gaming", "What is the primary currency used in the game Fallout?", ["Gold Coins", "Nuka-Cola Bottle Caps", "Credits", "Rupees"], 1, "Bottle caps from Nuka-Cola are the wasteland currency."),

    TriviaQuestion("Geography", "What is the capital city of Australia?", ["Sydney", "Melbourne", "Canberra", "Brisbane"], 2, "Canberra was chosen as the compromise capital between Sydney and Melbourne."),
    TriviaQuestion("Geography", "Which river is the longest in the world?", ["Amazon River", "Nile River", "Yangtze River", "Mississippi River"], 1, "The Nile River in Africa spans approximately 6,650 kilometers."),
    TriviaQuestion("Geography", "What country has the greatest number of natural lakes?", ["Canada", "Russia", "United States", "Finland"], 0, "Canada contains over 60% of all natural lakes on Earth."),
    TriviaQuestion("Geography", "Mount Kilimanjaro is the highest peak in which continent?", ["Asia", "South America", "Africa", "Europe"], 2, "Kilimanjaro is a dormant volcano in Tanzania, Africa at 5,895m."),
    TriviaQuestion("Geography", "What is the smallest independent country in the world by land area?", ["Monaco", "Nauru", "San Marino", "Vatican City"], 3, "Vatican City covers only 0.49 square kilometers."),

    TriviaQuestion("History", "In what year did the Titanic sink?", ["1905", "1912", "1918", "1923"], 1, "The RMS Titanic struck an iceberg and sank on April 15, 1912."),
    TriviaQuestion("History", "Who was the first person to walk on the Moon?", ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "Michael Collins"], 2, "Neil Armstrong stepped onto the lunar surface during Apollo 11 in July 1969."),
    TriviaQuestion("History", "Which ancient civilization constructed Machu Picchu?", ["Aztecs", "Mayans", "Incas", "Olmecs"], 2, "Machu Picchu was built by the Inca Empire in modern-day Peru."),
    TriviaQuestion("History", "What wall fell in November 1989, symbolizing the end of the Cold War?", ["Great Wall", "Berlin Wall", "Hadrian's Wall", "Antonine Wall"], 1, "The fall of the Berlin Wall occurred on November 9, 1989."),
    TriviaQuestion("History", "Who wrote the ancient Greek epic poems the 'Iliad' and the 'Odyssey'?", ["Socrates", "Homer", "Plato", "Aristotle"], 1, "Homer is traditionally credited with authoring both epics.")
]


class TriviaView(discord.ui.View):
    def __init__(self, author_id: int, question: TriviaQuestion, timeout: float = 20.0):
        super().__init__(timeout=timeout)
        self.author_id = author_id
        self.question = question
        self.answered = False
        self.user_choice: Optional[int] = None
        self._build_buttons()

    def _build_buttons(self) -> None:
        labels = ["A", "B", "C", "D"]
        for idx, option in enumerate(self.question.options):
            btn = discord.ui.Button(
                label=f"{labels[idx]}: {option}",
                style=discord.ButtonStyle.secondary,
                custom_id=f"trivia_{idx}",
                row=idx // 2
            )
            btn.callback = self._create_callback(idx)
            self.add_item(btn)

    def _create_callback(self, choice_idx: int):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.author_id:
                await interaction.response.send_message("Only the trivia contestant can answer!", ephemeral=True)
                return

            if self.answered:
                await interaction.response.send_message("You have already submitted your answer!", ephemeral=True)
                return

            self.answered = True
            self.user_choice = choice_idx
            is_correct = (choice_idx == self.question.correct_index)

            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
                    btn_idx = int(item.custom_id.split("_")[1])
                    if btn_idx == self.question.correct_index:
                        item.style = discord.ButtonStyle.success
                    elif btn_idx == choice_idx:
                        item.style = discord.ButtonStyle.danger

            embed = discord.Embed(
                title="🎯 Trivia — Result" if is_correct else "❌ Trivia — Incorrect",
                color=0x57F287 if is_correct else 0xED4245,
                description=f"**Question:** {self.question.question}\n\n"
                            f"**Your Answer:** {self.question.options[choice_idx]}\n"
                            f"**Correct Answer:** {self.question.options[self.question.correct_index]}\n\n"
                            f"💡 *{self.question.explanation}*"
            )
            embed.set_footer(text="Sentinel Trivia Engine")
            await interaction.response.edit_message(embed=embed, view=self)

        return callback

    def get_initial_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f"❓ Trivia — {self.question.category}",
            description=f"### {self.question.question}\n\nChoose the correct option below within 20 seconds!",
            color=0x5865F2
        )
        embed.set_footer(text="Sentinel Trivia Challenge")
        return embed
