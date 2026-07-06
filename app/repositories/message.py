from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy import delete, func, or_, select
from app.models.enums import MessageDirection
from app.models.message import Message
from app.repositories.base import BaseRepository

class MessageRepository(BaseRepository[Message]):
    model = Message
    async def list_for_chat(self, chat_id: int, limit: int = 50, offset: int = 0) -> list[Message]:
        r = await self.session.execute(select(Message).where(Message.chat_id == chat_id).order_by(Message.id.desc()).limit(limit).offset(offset))
        return list(r.scalars().all())
    async def search(self, *, q: str = "", chat_id: int | None = None, page: int = 1, page_size: int = 20) -> tuple[list[Message], int]:
        stmt = select(Message)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(or_(Message.text.ilike(like), Message.caption.ilike(like)))
        if chat_id is not None:
            stmt = stmt.where(Message.chat_id == chat_id)
        total = (await self.session.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
        r = await self.session.execute(stmt.order_by(Message.id.desc()).limit(page_size).offset((page-1)*page_size))
        return list(r.scalars().all()), total
    async def cleanup(self, days: int) -> int:
        cutoff = datetime.utcnow() - timedelta(days=days)
        r = await self.session.execute(delete(Message).where(Message.created_at < cutoff))
        return r.rowcount
    async def stats(self) -> dict:
        total = (await self.session.execute(select(func.count(Message.id)))).scalar_one()
        inc = (await self.session.execute(select(func.count(Message.id)).where(Message.direction == MessageDirection.INCOMING))).scalar_one()
        out = (await self.session.execute(select(func.count(Message.id)).where(Message.direction == MessageDirection.OUTGOING))).scalar_one()
        return {"total": total, "incoming": inc, "outgoing": out}
