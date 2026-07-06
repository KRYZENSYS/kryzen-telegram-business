"""Chat repository."""
from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.chat import Chat
from app.repositories.base import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    model = Chat

    async def get_by_telegram_id(self, business_id: int, telegram_chat_id: int) -> Chat | None:
        stmt = select(Chat).where(
            Chat.business_id == business_id, Chat.telegram_chat_id == telegram_chat_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_or_create(
        self,
        *,
        business_id: int,
        telegram_chat_id: int,
        chat_type: str = "private",
        title: str | None = None,
        username: str | None = None,
    ) -> tuple[Chat, bool]:
        existing = await self.get_by_telegram_id(business_id, telegram_chat_id)
        if existing:
            return existing, False
        chat = Chat(
            business_id=business_id,
            telegram_chat_id=telegram_chat_id,
            chat_type=chat_type,
            title=title,
            username=username,
        )
        await self.add(chat)
        return chat, True

    async def list_with_messages(self, business_id: int, *, limit: int = 100) -> Sequence[Chat]:
        stmt = (
            select(Chat)
            .where(Chat.business_id == business_id)
            .options(selectinload(Chat.messages))
            .order_by(Chat.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
