from __future__ import annotations
"""KRYZEN Telegram Business — unified entry point for Replit.
Runs FastAPI (uvicorn) and aiogram polling concurrently in a single process.
"""
import asyncio
import logging
import os
import sys

import uvicorn
from aiogram import Bot, Dispatcher
from fastapi import FastAPI

# Ensure /app is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config.logging import setup_logging
from app.config.settings import settings
from app.database.session import async_session_factory
from app.database.base import Base
from app.middlewares.db import DatabaseMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.middlewares.user import UserMiddleware
from app.models._registry import *  # noqa: F401  (registers all models)
from app.business.router import router as business_router
from app.handlers import register_all
from app.api.app import app as fastapi_app  # FastAPI instance
from app.utils.exceptions import AppError

setup_logging(settings.log_level)
logger = logging.getLogger("kryzen.main")


async def _init_db() -> None:
    """Create SQLite tables on first start (no Alembic needed for Replit demo)."""
    if not settings.database_url.startswith("sqlite"):
        return
    async with async_session_factory() as s:
        await s.run_sync(Base.metadata.create_all)
    logger.info("SQLite tables ready")


async def _run_bot() -> None:
    if not settings.bot_token:
        logger.error("BOT_TOKEN is not set. Set it in Replit Secrets.")
        return
    bot = Bot(token=settings.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    # Middlewares
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(UserMiddleware())
    dp.message.middleware(ThrottlingMiddleware(rate_limit_per_minute=settings.rate_limit_per_minute))
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    # Routers
    dp.include_router(business_router)
    register_all(dp)
    logger.info("Bot started (long polling)...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.exception("Bot crashed: %s", e)
    finally:
        await bot.session.close()


async def _run_api() -> None:
    config = uvicorn.Config(
        fastapi_app,
        host=settings.app_host or "0.0.0.0",
        port=int(os.environ.get("APP_PORT", settings.app_port or 8080)),
        log_level=settings.log_level.lower(),
        access_log=False,
    )
    server = uvicorn.Server(config)
    logger.info("API starting on %s:%s", config.host, config.port)
    await server.serve()


async def _amain() -> None:
    await _init_db()
    if not settings.bot_token:
        logger.warning("BOT_TOKEN missing — running API only. Set it in Replit Secrets to enable bot.")
        await _run_api()
        return
    await asyncio.gather(_run_bot(), _run_api())


def main() -> None:
    try:
        asyncio.run(_amain())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopped by user")
    except AppError as e:
        logger.error("App error: %s", e)


if __name__ == "__main__":
    main()
