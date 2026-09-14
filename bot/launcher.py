import asyncio
import logging
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import TOKEN, API_ENABLED, API_PORT, BOT_NAME


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)-25s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root.addHandler(handler)

    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)


def start_api(bot):
    if not API_ENABLED:
        return
    try:
        import uvicorn
        from api.app import create_app
        app = create_app(bot)
        config = uvicorn.Config(app, host="0.0.0.0", port=API_PORT, log_level="warning")
        server = uvicorn.Server(config)

        thread = threading.Thread(target=server.run, daemon=True, name="api-server")
        thread.start()
        logging.getLogger("Wutherer").info("API server started on port %d", API_PORT)
    except Exception as e:
        logging.getLogger("Wutherer").error("Failed to start API server: %s", e)


async def main():
    setup_logging()
    log = logging.getLogger("Wutherer")

    if not TOKEN:
        log.critical("No bot token found. Set TOKEN in your .env file.")
        sys.exit(1)

    from core.bot import WuthererBot
    bot = WuthererBot()

    log.info("Starting %s...", BOT_NAME)
    start_api(bot)

    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        log.info("Shutting down...")
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

