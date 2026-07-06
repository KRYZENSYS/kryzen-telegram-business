from __future__ import annotations
from sqlalchemy import select
from app.models.subscription import Subscription
from app.repositories.base import BaseRepository

class SubscriptionRepository(BaseRepository[Subscription]):
    model = Subscription
    async def active_for(self, user_id: int) -> Subscription | None:
        r = await self.session.execute(select(Subscription).where(Subscription.user_id == user_id).order_by(Subscription.id.desc()))
        return r.scalars().first()
