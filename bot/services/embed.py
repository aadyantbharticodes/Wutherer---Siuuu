from __future__ import annotations
import datetime
from typing import Optional, Any
import discord

from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR, BOT_COLOR_WARNING, BOT_NAME


class EmbedBuilder:

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: int = BOT_COLOR,
        timestamp: bool = True
    ):
        self.embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.now(datetime.timezone.utc) if timestamp else None
        )

    @classmethod
    def default(cls, title: Optional[str] = None, description: Optional[str] = None) -> EmbedBuilder:
        return cls(title=title, description=description, color=BOT_COLOR)

    @classmethod
    def success(cls, title: Optional[str] = None, description: Optional[str] = None) -> EmbedBuilder:
        return cls(title=title, description=description, color=BOT_COLOR_SUCCESS)

    @classmethod
    def error(cls, title: Optional[str] = None, description: Optional[str] = None) -> EmbedBuilder:
        return cls(title=title, description=description, color=BOT_COLOR_ERROR)

    @classmethod
    def warning(cls, title: Optional[str] = None, description: Optional[str] = None) -> EmbedBuilder:
        return cls(title=title, description=description, color=BOT_COLOR_WARNING)

    def set_author(self, name: str, icon_url: Optional[str] = None, url: Optional[str] = None) -> EmbedBuilder:
        self.embed.set_author(name=name, icon_url=icon_url, url=url)
        return self

    def set_footer(self, text: Optional[str] = None, icon_url: Optional[str] = None) -> EmbedBuilder:
        footer_text = text or f"{BOT_NAME} • Automated Server Intelligence"
        self.embed.set_footer(text=footer_text, icon_url=icon_url)
        return self

    def set_thumbnail(self, url: str) -> EmbedBuilder:
        self.embed.set_thumbnail(url=url)
        return self

    def set_image(self, url: str) -> EmbedBuilder:
        self.embed.set_image(url=url)
        return self

    def add_field(self, name: str, value: Any, inline: bool = False) -> EmbedBuilder:
        self.embed.add_field(name=str(name)[:256], value=str(value)[:1024], inline=inline)
        return self

    def build(self) -> discord.Embed:
        if not self.embed.footer.text:
            self.set_footer()
        return self.embed

