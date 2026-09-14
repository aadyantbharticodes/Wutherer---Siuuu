import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "wutherer.db"
ASSETS_DIR = BASE_DIR / "assets"
FONT_DIR = ASSETS_DIR / "fonts"

TOKEN = os.getenv("TOKEN", "")
BOT_NAME = os.getenv("BOT_NAME", "Wutherer")
DEFAULT_PREFIX = os.getenv("DEFAULT_PREFIX", "s!")
BOT_COLOR = 0x6C5CE7
BOT_COLOR_SUCCESS = 0x00B894
BOT_COLOR_ERROR = 0xD63031
BOT_COLOR_WARNING = 0xFDAA18
BOT_COLOR_INFO = 0x0984E3

SUPPORT_SERVER = os.getenv("SUPPORT_SERVER", "")
BOT_INVITE = os.getenv("BOT_INVITE", "")


def _parse_ids(key: str) -> list[int]:
    raw = os.getenv(key, "").strip()
    if not raw:
        return []
    return [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]


OWNER_IDS: list[int] = _parse_ids("OWNER_IDS")

LAVALINK_HOST = os.getenv("LAVALINK_HOST", "")
LAVALINK_PORT = int(os.getenv("LAVALINK_PORT", "2333"))
LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD", "youshallnotpass")
LAVALINK_SECURE = os.getenv("LAVALINK_SECURE", "false").lower() == "true"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
AI_ENABLED = bool(GEMINI_API_KEY)
AI_MODEL = os.getenv("AI_MODEL", "gemini-2.0-flash")
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2048"))
AI_RATE_LIMIT = int(os.getenv("AI_RATE_LIMIT_PER_MIN", "15"))

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_ENABLED = bool(YOUTUBE_API_KEY)
YOUTUBE_CHECK_INTERVAL = int(os.getenv("YOUTUBE_CHECK_INTERVAL", "300"))

HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY", "")

API_ENABLED = os.getenv("API_ENABLED", "true").lower() == "true"
API_PORT = int(os.getenv("API_PORT", "8000"))
API_KEY = os.getenv("DASHBOARD_API_KEY", "")
CORS_ORIGINS = list(dict.fromkeys([
    "http://localhost:3000",
    "https://localhost:3000",
    *(o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()),
]))

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

MAX_WARNS = 5
DEFAULT_WARN_PUNISHMENT = "timeout"
DEFAULT_TIMEOUT_DURATION = 600
XP_PER_MESSAGE = (15, 25)
XP_COOLDOWN = 60
LEVEL_FORMULA_BASE = 100
LEVEL_FORMULA_MULTIPLIER = 1.5

CAPTCHA_FONTS = [str(FONT_DIR / "arial.ttf")]
CAPTCHA_LENGTH = 6
CAPTCHA_WIDTH = 280
CAPTCHA_HEIGHT = 90

