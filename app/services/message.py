from __future__ import annotations
import logging
from app.models.message import Message
from app.repositories.message import MessageRepository
logger = logging.getLogger(__name__)
class MessageService:
    def __init__(self, repo: MessageRepository) -> None: self.repo = repo
    async def save(self, **kwargs) -> Message:
        m = Message(**kwargs); return await self.repo.add(m)
    async def list_for_chat(self, chat_id: int, limit=50, offset=0): return await self.repo.list_for_chat(chat_id, limit, offset)
    async def search(self, **kwargs): return await self.repo.search(**kwargs)
    async def cleanup(self, days: int) -> int: return await self.repo.cleanup(days)
    async def stats(self) -> dict: return await self.repo.stats()
