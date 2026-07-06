from aiogram import Dispatcher
from app.handlers.start import router as start_router
from app.handlers.menu import router as menu_router
from app.handlers.business import router as biz_router
from app.handlers.rules import router as rules_router
from app.handlers.ai import router as ai_router
from app.handlers.promo import router as promo_router
from app.handlers.admin import router as admin_router
from app.handlers.fallback import router as fallback_router

def register_all(dp: Dispatcher) -> None:
    for r in (start_router, menu_router, biz_router, rules_router, ai_router, promo_router, admin_router, fallback_router):
        dp.include_router(r)
