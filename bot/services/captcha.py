from __future__ import annotations
import io
import math
import random
import string
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class CaptchaService:

    CHARACTERS = string.ascii_uppercase.replace("O", "").replace("I", "") + "23456789"

    @classmethod
    def generate_text_captcha(cls, length: int = 5, difficulty: str = "medium") -> Tuple[str, io.BytesIO]:
        code = "".join(random.choices(cls.CHARACTERS, k=length))
        width, height = 300, 100
        image = Image.new("RGB", (width, height), color=(20, 20, 30))
        draw = ImageDraw.Draw(image)


        num_lines = 8 if difficulty == "hard" else (5 if difficulty == "medium" else 3)
        for _ in range(num_lines):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            color = (random.randint(60, 140), random.randint(60, 140), random.randint(180, 250))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=random.randint(1, 3))


        for _ in range(300):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill=(random.randint(80, 180), random.randint(80, 180), random.randint(80, 180)))


        font_size = 40
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        char_spacing = (width - 60) // length
        for i, char in enumerate(code):
            char_img = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
            char_draw = ImageDraw.Draw(char_img)
            char_color = (
                random.randint(180, 255),
                random.randint(180, 255),
                random.randint(220, 255),
                255
            )
            char_draw.text((15, 5), char, font=font, fill=char_color)
            rotated = char_img.rotate(random.randint(-30, 30), expand=1, resample=Image.BILINEAR)
            image.paste(rotated, (30 + i * char_spacing, random.randint(15, 30)), rotated)


        if difficulty in ("medium", "hard"):
            image = image.filter(ImageFilter.SMOOTH_MORE)

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return code, buffer

    @classmethod
    def generate_math_captcha(cls) -> Tuple[str, str, io.BytesIO]:
        a = random.randint(3, 20)
        b = random.randint(2, 15)
        op = random.choice(["+", "-"])
        if op == "+":
            ans = a + b
            q = f"{a} + {b} = ?"
        else:
            if a < b:
                a, b = b, a
            ans = a - b
            q = f"{a} - {b} = ?"

        width, height = 280, 80
        image = Image.new("RGB", (width, height), color=(25, 25, 35))
        draw = ImageDraw.Draw(image)

        for _ in range(4):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            draw.line([(x1, y1), (x2, y2)], fill=(80, 70, 120), width=2)

        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            font = ImageFont.load_default()

        draw.text((40, 20), q, font=font, fill=(220, 220, 255))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return q, str(ans), buffer

