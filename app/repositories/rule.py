"""Rule repository."""
from __future__ import annotations

from typing import Sequence

from sqlalchemy import select, update

from app.models.enums import RuleSource
from app.models.rule import Rule
from app.repositories.base import BaseRepository


class RuleRepository(BaseRepository[Rule]):
    model = Rule

    async def list_active_for_user(
        self, user_id: int, *, source: RuleSource | None = None
    ) -> Sequence[Rule]:
        stmt = (
            select(Rule)
            .where(Rule.user_id == user_id, Rule.is_active.is_(True))
            .order_by(Rule.priority.asc(), Rule.created_at.asc())
        )
        if source is not None:
            stmt = stmt.where(Rule.source == source)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_by_user(self, user_id: int) -> Sequence[Rule]:
        stmt = select(Rule).where(Rule.user_id == user_id).order_by(Rule.priority.asc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def increment_match(self, rule_id: int) -> None:
        await self.session.execute(
            update(Rule).where(Rule.id == rule_id).values(match_count=Rule.match_count + 1)
        )
