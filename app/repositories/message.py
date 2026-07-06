"""Message repository."""
from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import and_, func, or_, select

from app.models.enums import MessageDirection, MessageType
from app.models.message import Message
from app.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    model = Message

    async def list_by_chat(
        self,
        chat_id: int,
        *,
        limit: int = 50,
        offset: int = 0,
        direction: MessageDirection | None = None,
    ) -> Sequence[Message]:
        stmt = select(Message).where(Message.chat_id == chat_id)
        if direction:
            stmt = stmt.where(Message.direction == direction)
        stmt = stmt.order_by(Message.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search(
        self,
        *,
        chat_id: int | None = None,
        business_owner_id: int | None = None,
        text_query: str | None = None,
        direction: MessageDirection | None = None,
        message_type: MessageType | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[Sequence[Message], int]:
        stmt = select(Message)
        conditions = []
        if chat_id is not None:
            conditions.append(Message.chat_id == chat_id)
        if business_owner_id is not None:
            from app.models.chat import Chat
            from app.models.business import Business
            stmt = stmt.join(Chat, Message.chat_id == Chat.id).join(Business, Chat.business_id == Business.id)
            conditions.append(Business.owner_id == business_owner_id)
        if text_query:
            like = f"%{text_query}%"
            conditions.append(or_(Message.text.ilike(like), Message.caption.ilike(like)))
        if direction:
            conditions.append(Message.direction == direction)
        if message_type:
            conditions.append(Message.message_type == message_type)
        if date_from:
            conditions.append(Message.created_at >= date_from)
        if date_to:
            conditions.append(Message.created_at <= date_to)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = int((await self.session.execute(total_stmt)).scalar_one() or 0)

        stmt = stmt.order_by(Message.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all(), total

    async def stats(self, owner_id: int | None = None) -> dict:
        stmt = select(
            func.count().label("total"),
            func.sum(func.case((Message.direction == MessageDirection.INCOMING, 1), else_=0)).label("incoming"),
            func.sum(func.case((Message.direction == MessageDirection.OUTGOING, 1), else_=0)).label("outgoing"),
        )
        if owner_id is not None:
            from app.models.chat import Chat
            from app.models.business import Business
            stmt = stmt.join(Chat, Message.chat_id == Chat.id).join(Business, Chat.business_id == Business.id).where(Business.owner_id == owner_id)
        row = (await self.session.execute(stmt)).one()

        by_type_stmt = select(Message.message_type, func.count()).group_by(Message.message_type)
        if owner_id is not None:
            from app.models.chat import Chat
            from app.models.business import Business
            by_type_stmt = by_type_stmt.join(Chat, Message.chat_id == Chat.id).join(Business, Chat.business_id == Business.id).where(Business.owner_id == owner_id)
        by_type_rows = (await self.session.execute(by_type_stmt)).all()

        return {
            "total": int(row.total or 0),
            "incoming": int(row.incoming or 0),
            "outgoing": int(row.outgoing or 0),
            "by_type": {str(k): int(v) for k, v in by_type_rows},
        }

    async def cleanup_older_than(self, days: int) -> int:
        from sqlalchemy import delete as sql_delete
        cutoff_ts = datetime.utcnow().timestamp() - days * 86400
        cutoff_dt = datetime.utcfromtimestamp(cutoff_ts)
        result = await self.session.execute(
            sql_delete(Message).where(Message.created_at < cutoff_dt)
        )
        return int(result.rowcount or 0)
