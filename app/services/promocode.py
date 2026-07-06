from __future__ import annotations
import logging
from datetime import datetime
from app.models.enums import SubscriptionPlan
from app.models.promocode import PromoCode
from app.repositories.promocode import PromoCodeRepository
from app.repositories.user import UserRepository
from app.services.subscription import SubscriptionService
from app.utils.exceptions import NotFoundError, ValidationError, ConflictError
logger = logging.getLogger(__name__)
class PromoCodeService:
    def __init__(self, promos: PromoCodeRepository, users: UserRepository, subs) -> None:
        self.promos = promos; self.users = users; self.subs = subs
    async def create(self, data, *, created_by: int) -> PromoCode:
        code = data.code.upper()
        if await self.promos.get_by_code(code): raise ConflictError("Code already exists")
        p = PromoCode(code=code, description=data.description, discount_percent=data.discount_percent,
                      discount_amount=data.discount_amount, bonus_days=data.bonus_days,
                      max_uses=data.max_uses, max_per_user=data.max_per_user,
                      starts_at=data.starts_at, expires_at=data.expires_at, is_active=data.is_active,
                      created_by=created_by)
        return await self.promos.add(p)
    async def redeem(self, *, code: str, user_id: int) -> dict:
        promo = await self.promos.get_by_code(code)
        if not promo or not promo.is_active: raise NotFoundError("Promo code not found or inactive")
        now = datetime.utcnow()
        if promo.starts_at and promo.starts_at > now: raise ValidationError("Promo not started yet")
        if promo.expires_at and promo.expires_at < now: raise ValidationError("Promo expired")
        if promo.max_uses and promo.used_count >= promo.max_uses: raise ValidationError("Promo exhausted")
        if await self.promos.count_user_redemptions(promo.id, user_id) >= promo.max_per_user:
            raise ValidationError("You already used this code")
        await self.promos.add_redemption(promo.id, user_id)
        promo.used_count += 1
        if self.subs and promo.bonus_days > 0:
            await self.subs.activate(user_id=user_id, plan=self._best_plan_for_bonus(promo.bonus_days),
                                     days=promo.bonus_days, promo_code=promo.code)
        return {"code": promo.code, "bonus_days": promo.bonus_days,
                "discount_percent": promo.discount_percent, "discount_amount": promo.discount_amount}
    @staticmethod
    def _best_plan_for_bonus(days: int):
        return SubscriptionPlan.PREMIUM if days <= 365 else SubscriptionPlan.BUSINESS
