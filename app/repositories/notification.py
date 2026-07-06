"""Notification repository."""
from __future__ import annotations

from sqlalchemy import select, update

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    model = Notification

    async def list_unread(self, user_id: int, *, limit: int = 50) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        return list((await self.session.execute(stmt)).scalars().all())

    async def mark_read(self, notification_id: int) -> None:
        await self.session.execute(
            update(Notification).where(Notification.id == notification_id).values(is_read=True)
        )

    async def mark_all_read(self, user_id: int) -> None:
        await self.session.execute(
            update(Notification).where(Notification.user_id == user_id).values(is_read=True)
        )
