from __future__ import annotations
import logging
from app.models.notification import Notification
from app.repositories.notification import NotificationRepository
logger = logging.getLogger(__name__)
class NotificationService:
    def __init__(self, repo: NotificationRepository) -> None: self.repo = repo
    async def push(self, *, user_id, type, title: str, body: str, payload=None) -> Notification:
        n = Notification(user_id=user_id, type=type, title=title, body=body, payload=payload)
        return await self.repo.add(n)
    async def list_unread(self, user_id: int): return await self.repo.unread_for(user_id)
    async def mark_read(self, notification_id: int) -> None:
        n = await self.repo.get(notification_id)
        if n: n.is_read = True
