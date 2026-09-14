from __future__ import annotations

import io
from typing import Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class WelcomeCardGenerator:

    WIDTH = 1024
    HEIGHT = 450
    CARD_BG = (13, 14, 21, 240)
    BORDER_COLOR = (108, 92, 231, 200)
    ACCENT_COLOR = (162, 155, 254)
    TEXT_WHITE = (255, 255, 255)
    TEXT_MUTED = (160, 164, 184)

    @classmethod
    def create_card(
        cls,
        member_name: str,
        guild_name: str,
        member_count: int,
        avatar_bytes: Optional[bytes] = None,
    ) -> io.BytesIO:

        base = Image.new("RGBA", (cls.WIDTH, cls.HEIGHT), (10, 11, 16, 255))
        draw = ImageDraw.Draw(base)


        for y in range(cls.HEIGHT):
            alpha = int(30 * (1 - y / cls.HEIGHT))
            draw.line([(0, y), (cls.WIDTH, y)], fill=(108, 92, 231, alpha))


        margin = 25
        card_box = [margin, margin, cls.WIDTH - margin, cls.HEIGHT - margin]
        card = Image.new("RGBA", (cls.WIDTH, cls.HEIGHT), (0, 0, 0, 0))
        card_draw = ImageDraw.Draw(card)
        card_draw.rounded_rectangle(card_box, radius=24, fill=cls.CARD_BG, outline=cls.BORDER_COLOR, width=3)
        base = Image.alpha_composite(base, card)
        draw = ImageDraw.Draw(base)


        avatar_size = 180
        avatar_x = 80
        avatar_y = (cls.HEIGHT - avatar_size) // 2


        glow_box = [avatar_x - 8, avatar_y - 8, avatar_x + avatar_size + 8, avatar_y + avatar_size + 8]
        draw.ellipse(glow_box, outline=cls.BORDER_COLOR, width=4)

        if avatar_bytes:
            try:
                raw_avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
                raw_avatar = raw_avatar.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
                mask = Image.new("L", (avatar_size, avatar_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
                base.paste(raw_avatar, (avatar_x, avatar_y), mask)
            except Exception:

                draw.ellipse([avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size], fill=(45, 52, 54))
        else:
            draw.ellipse([avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size], fill=(45, 52, 54))


        text_x = avatar_x + avatar_size + 60
        title_y = 110
        name_y = 175
        server_y = 250
        counter_y = 310


        try:
            font_title = ImageFont.truetype("arial.ttf", 28)
            font_name = ImageFont.truetype("arialbd.ttf", 44)
            font_sub = ImageFont.truetype("arial.ttf", 26)
            font_badge = ImageFont.truetype("arialbd.ttf", 22)
        except IOError:
            font_title = font_name = font_sub = font_badge = ImageFont.load_default()


        draw.text((text_x, title_y), "WELCOME TO", fill=cls.ACCENT_COLOR, font=font_title)


        display_name = member_name if len(member_name) <= 20 else member_name[:18] + "..."
        draw.text((text_x, name_y), display_name, fill=cls.TEXT_WHITE, font=font_name)


        display_guild = guild_name if len(guild_name) <= 26 else guild_name[:24] + "..."
        draw.text((text_x, server_y), display_guild, fill=cls.TEXT_MUTED, font=font_sub)


        badge_text = f"Member #{member_count:,}"
        pill_w = 180
        pill_h = 42
        pill_box = [text_x, counter_y, text_x + pill_w, counter_y + pill_h]
        draw.rounded_rectangle(pill_box, radius=12, fill=(108, 92, 231, 80), outline=cls.BORDER_COLOR, width=2)
        draw.text((text_x + 20, counter_y + 10), badge_text, fill=cls.ACCENT_COLOR, font=font_badge)

        buf = io.BytesIO()
        base.save(buf, format="PNG", optimize=True)
        buf.seek(0)
        return buf

