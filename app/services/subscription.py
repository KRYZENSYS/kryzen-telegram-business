from __future__ import annotations
import logging
from datetime import datetime, timedelta
from app.models.enums import SubscriptionPlan, SubscriptionStatus
from app.models.subscription import Subscription
from app.repositories.subscription import SubscriptionRepository
from app.repositories.user import UserRepository
logger = logging.getLogger(__name__)
PLAN_DAYS = {SubscriptionPlan.FREE: 0, SubscriptionPlan.PREMIUM: 30, SubscriptionPlan.BUSINESS: 365}
class SubscriptionService:
    def __init__(self, repo: SubscriptionRepository, users: UserRepository) -> None:
        self.repo = repo; self.users = users
    async def activate(self, *, user_id, plan: SubscriptionPlan, days=None, promo_code=None, amount=0.0) -> Subscription:
        actual_days = days if days is not None else PLAN_DAYS.get(plan, 30)
        sub = Subscription(user_id=user_id, plan=plan, status=SubscriptionStatus.ACTIVE,
                           started_at=datetime.utcnow(), expires_at=datetime.utcnow() + timedelta(days=actual_days),
                           promo_code=promo_code, amount=amount, currency="USD")
        return await self.repo.add(sub)
    async def cancel(self, subscription_id: int) -> None:
        s = await self.repo.get(subscription_id)
        if s: s.status = SubscriptionStatus.CANCELLED; s.cancelled_at = datetime.utcnow()
    async def is_premium(self, user_id: int) -> bool:
        sub = await self.repo.active_for(user_id)
        return bool(sub and sub.expires_at > datetime.utcnow())
