from __future__ import annotations
from sqlalchemy import func, select
from app.models.promocode import PromoCode, PromoRedemption
from app.repositories.base import BaseRepository

class PromoCodeRepository(BaseRepository[PromoCode]):
    model = PromoCode
    async def get_by_code(self, code: str) -> PromoCode | None:
        r = await self.session.execute(select(PromoCode).where(PromoCode.code == code.upper()))
        return r.scalar_one_or_none()
    async def list_active(self) -> list[PromoCode]:
        r = await self.session.execute(select(PromoCode).where(PromoCode.is_active == True).order_by(PromoCode.id.desc()))
        return list(r.scalars().all())
    async def count_user_redemptions(self, promo_id: int, user_id: int) -> int:
        r = await self.session.execute(select(func.count(PromoRedemption.id)).where(
            PromoRedemption.promo_id == promo_id, PromoRedemption.user_id == user_id))
        return r.scalar_one()
    async def add_redemption(self, promo_id: int, user_id: int) -> None:
        self.session.add(PromoRedemption(promo_id=promo_id, user_id=user_id))
        await self.session.flush()

class PromoRedemptionRepository(BaseRepository[PromoRedemption]):
    model = PromoRedemption
