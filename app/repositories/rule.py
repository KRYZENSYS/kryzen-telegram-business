from __future__ import annotations
from sqlalchemy import and_, select
from app.models.rule import Rule
from app.repositories.base import BaseRepository

class RuleRepository(BaseRepository[Rule]):
    model = Rule
    async def list_for_user(self, user_id: int) -> list[Rule]:
        r = await self.session.execute(select(Rule).where(Rule.user_id == user_id).order_by(Rule.priority.asc(), Rule.id.asc()))
        return list(r.scalars().all())
    async def list_active_for_user(self, user_id: int) -> list[Rule]:
        r = await self.session.execute(select(Rule).where(and_(Rule.user_id == user_id, Rule.is_active == True)).order_by(Rule.priority.asc(), Rule.id.asc()))
        return list(r.scalars().all())
