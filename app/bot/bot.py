from __future__ import annotations
from aiogram import Bot, Dispatcher
from app.config.settings import settings

bot: Bot | None = None
dispatcher: Dispatcher | None = None

def get_bot() -> Bot:
    global bot
    if bot is None:
        if not settings.bot_token: raise RuntimeError("BOT_TOKEN not configured")
        bot = Bot(token=settings.bot_token, parse_mode="HTML")
    return bot

def get_dispatcher() -> Dispatcher:
    global dispatcher
    if dispatcher is None: dispatcher = Dispatcher()
    return dispatcher
