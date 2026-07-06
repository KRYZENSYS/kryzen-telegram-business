from __future__ import annotations
from sqlalchemy import delete, func, select
from app.models.ai_history import AIHistory
from app.repositories.base import BaseRepository

class AIHistoryRepository(BaseRepository[AIHistory]):
    model = AIHistory
    async def recent(self, chat_id: int, limit: int = 20) -> list[AIHistory]:
        r = await self.session.execute(select(AIHistory).where(AIHistory.chat_id == chat_id).order_by(AIHistory.id.desc()).limit(limit))
        return list(r.scalars().all())
    async def clear_for_chat(self, chat_id: int) -> int:
        r = await self.session.execute(delete(AIHistory).where(AIHistory.chat_id == chat_id))
        return r.rowcount
    async def stats(self) -> dict:
        total = (await self.session.execute(select(func.count(AIHistory.id)))).scalar_one()
        tokens = (await self.session.execute(select(func.coalesce(func.sum(AIHistory.total_tokens), 0)))).scalar_one()
        return {"requests": total, "tokens": int(tokens)}
