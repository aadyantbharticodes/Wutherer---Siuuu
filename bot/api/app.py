from __future__ import annotations
import logging
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import BOT_NAME
from api.middleware import RequestLoggingMiddleware
from api.routes import all_routers

log = logging.getLogger("wutherer.api")


def create_app(bot=None) -> FastAPI:
    app = FastAPI(
        title=f"{BOT_NAME} Control Panel API",
        version="2.0.0",
        description="REST API powering the Sentinel Discord dashboard and integrations.",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.state.bot = bot


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestLoggingMiddleware)


    for router in all_routers:
        app.include_router(router, prefix="/api")

    log.info("Sentinel FastAPI app initialized with %d routers", len(all_routers))
    return app

