from __future__ import annotations
import io
import math
from typing import Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import aiohttp


class ImageService:

    @staticmethod
    async def fetch_image(session: aiohttp.ClientSession, url: str) -> Optional[Image.Image]:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    return Image.open(io.BytesIO(data)).convert("RGBA")
        except Exception:
            pass
        return None

    @staticmethod
    def circle_crop(img: Image.Image) -> Image.Image:
        size = min(img.size)
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        output = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
        output.putalpha(mask)
        return output

    @staticmethod
    def apply_filter(img: Image.Image, filter_name: str) -> io.BytesIO:
        res = img.copy()
        f = filter_name.lower()
        if f == "grayscale":
            res = res.convert("L").convert("RGBA")
        elif f == "invert":
            rgb = res.convert("RGB")
            inv = ImageOps.invert(rgb)
            res = inv.convert("RGBA")
        elif f == "blur":
            res = res.filter(ImageFilter.GaussianBlur(radius=5))
        elif f == "contour":
            res = res.filter(ImageFilter.CONTOUR)
        elif f == "sepia":
            gray = res.convert("L")
            res = ImageOps.colorize(gray, black="#2e1f0c", white="#ffd79e").convert("RGBA")

        buffer = io.BytesIO()
        res.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @staticmethod
    def render_rank_card(
        username: str,
        avatar_img: Optional[Image.Image],
        level: int,
        xp: int,
        xp_needed: int,
        rank: int
    ) -> io.BytesIO:
        width, height = 800, 240
        card = Image.new("RGBA", (width, height), (18, 16, 28, 255))
        draw = ImageDraw.Draw(card)


        draw.rectangle([(2, 2), (width - 3, height - 3)], outline=(108, 92, 231, 120), width=2)


        if avatar_img:
            avatar = ImageService.circle_crop(avatar_img).resize((160, 160))
            card.paste(avatar, (35, 40), avatar)
        else:
            draw.ellipse([(35, 40), (195, 200)], fill=(108, 92, 231))


        try:
            name_font = ImageFont.truetype("arial.ttf", 34)
            info_font = ImageFont.truetype("arial.ttf", 22)
            small_font = ImageFont.truetype("arial.ttf", 18)
        except IOError:
            name_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
            small_font = ImageFont.load_default()


        draw.text((220, 45), username[:18], font=name_font, fill=(255, 255, 255))
        draw.text((width - 180, 45), f"RANK #{rank}", font=name_font, fill=(108, 92, 231))
        draw.text((220, 100), f"LEVEL {level}", font=info_font, fill=(162, 155, 254))
        draw.text((width - 240, 100), f"{xp:,} / {xp_needed:,} XP", font=info_font, fill=(200, 200, 220))


        bar_x, bar_y = 220, 155
        bar_w, bar_h = 530, 32
        draw.rectangle([(bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h)], fill=(35, 32, 50), outline=(50, 46, 75))
        ratio = min(1.0, max(0.0, xp / max(1, xp_needed)))
        progress_w = int(bar_w * ratio)
        if progress_w > 0:
            draw.rectangle([(bar_x, bar_y), (bar_x + progress_w, bar_y + bar_h)], fill=(108, 92, 231))

        buffer = io.BytesIO()
        card.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

