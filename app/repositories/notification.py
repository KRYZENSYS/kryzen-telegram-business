from __future__ import annotations
from sqlalchemy import select
from app.models.notification import Notification
from app.repositories.base import BaseRepository

class NotificationRepository(BaseRepository[Notification]):
    model = Notification
    async def unread_for(self, user_id: int, limit: int = 20) -> list[Notification]:
        r = await self.session.execute(select(Notification).where(Notification.user_id == user_id, Notification.is_read == False).order_by(Notification.id.desc()).limit(limit))
        return list(r.scalars().all())
