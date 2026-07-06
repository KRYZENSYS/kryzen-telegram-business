from __future__ import annotations
from datetime import datetime
from sqlalchemy import select
from app.models.business import Business
from app.models.enums import BusinessStatus
from app.repositories.base import BaseRepository

class BusinessRepository(BaseRepository[Business]):
    model = Business
    async def get_by_connection_id(self, connection_id: str) -> Business | None:
        r = await self.session.execute(select(Business).where(Business.business_connection_id == connection_id))
        return r.scalar_one_or_none()
    async def list_for_user(self, user_id: int) -> list[Business]:
        r = await self.session.execute(select(Business).where(Business.user_id == user_id).order_by(Business.id.desc()))
        return list(r.scalars().all())
    async def disconnect(self, business_id: int) -> None:
        biz = await self.get(business_id)
        if biz:
            biz.status = BusinessStatus.DISCONNECTED
            biz.enabled = False
            biz.disconnected_at = datetime.utcnow()
            await self.session.flush()
