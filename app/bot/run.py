from __future__ import annotations
import asyncio, logging
from app.bot.bot import get_bot, get_dispatcher
from app.config.logging import setup_logging
from app.config.settings import settings
from app.handlers import register_all
from app.middlewares.db import DatabaseMiddleware
from app.middlewares.user import UserMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.models._registry import *  # noqa
from app.business.router import router as business_router

logger = logging.getLogger(__name__)

async def main() -> None:
    setup_logging(settings.log_level)
    bot = get_bot(); dp = get_dispatcher()
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(UserMiddleware())
    dp.message.middleware(ThrottlingMiddleware(rate_limit_per_minute=settings.rate_limit_per_minute))
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    dp.include_router(business_router)
    register_all(dp)
    logger.info("Bot starting (long polling) ...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try: asyncio.run(main())
    except (KeyboardInterrupt, SystemExit): logger.info("Bot stopped")
