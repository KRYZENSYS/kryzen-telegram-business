from __future__ import annotations
from sqlalchemy import select
from app.models.chat import Chat
from app.repositories.base import BaseRepository

class ChatRepository(BaseRepository[Chat]):
    model = Chat
    async def get_or_create(self, *, business_id: int, telegram_chat_id: int, **kwargs) -> tuple[Chat, bool]:
        r = await self.session.execute(select(Chat).where(Chat.business_id == business_id, Chat.telegram_chat_id == telegram_chat_id))
        chat = r.scalar_one_or_none()
        if chat: return chat, False
        chat = Chat(business_id=business_id, telegram_chat_id=telegram_chat_id, **kwargs)
        self.session.add(chat); await self.session.flush()
        return chat, True
