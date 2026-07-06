from __future__ import annotations
from typing import Any, Dict
from aiogram import BaseMiddleware
from app.repositories.user import UserRepository
from app.services.user import UserService

class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: Dict[str, Any]) -> Any:
        tg_user = data.get("event_from_user")
        session = data.get("session")
        if tg_user and session:
            users = UserRepository(session)
            svc = UserService(users)
            user, _ = await svc.get_or_create(telegram_id=tg_user.id,
                username=tg_user.username, first_name=tg_user.first_name,
                last_name=tg_user.last_name, language_code=tg_user.language_code)
            data["db_user"] = user
            data["user_service"] = svc
        return await handler(event, data)
