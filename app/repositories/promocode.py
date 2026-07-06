"""Promo code repository."""
from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import func, select, update

from app.models.promocode import PromoCode, PromoCodeRedemption
from app.repositories.base import BaseRepository


class PromoCodeRepository(BaseRepository[PromoCode]):
    model = PromoCode

    async def get_by_code(self, code: str) -> PromoCode | None:
        return await self.get_by(code=code.upper())

    async def list_active(self) -> Sequence[PromoCode]:
        stmt = (
            select(PromoCode)
            .where(PromoCode.is_active.is_(True))
            .order_by(PromoCode.created_at.desc())
        )
        return (await self.session.execute(stmt)).scalars().all()

    async def increment_used(self, promo_id: int) -> None:
        await self.session.execute(
            update(PromoCode)
            .where(PromoCode.id == promo_id)
            .values(used_count=PromoCode.used_count + 1)
        )

    async def user_redemption_count(self, promo_id: int, user_id: int) -> int:
        stmt = select(func.count()).select_from(PromoCodeRedemption).where(
            PromoCodeRedemption.promo_id == promo_id,
            PromoCodeRedemption.user_id == user_id,
        )
        return int((await self.session.execute(stmt)).scalar_one() or 0)

    async def record_redemption(self, promo_id: int, user_id: int) -> None:
        self.session.add(
            PromoCodeRedemption(promo_id=promo_id, user_id=user_id, redeemed_at=datetime.utcnow())
        )
        await self.session.flush()


class AIHistoryRepository(BaseRepository):  # type: ignore[type-arg]
    from app.models.ai_history import AIHistory
    model = AIHistory

    async def last_n(self, chat_id: int, n: int) -> list[AIHistory]:
        stmt = (
            select(AIHistory)
            .where(AIHistory.chat_id == chat_id)
            .order_by(AIHistory.created_at.desc())
            .limit(n)
        )
        rows = list((await self.session.execute(stmt)).scalars().all())
        rows.reverse()
        return rows
