from __future__ import annotations
from typing import Any, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from app.database.session import async_session_factory

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: Dict[str, Any]) -> Any:
        async with async_session_factory() as session:
            data["session"] = session
            return await handler(event, data)
