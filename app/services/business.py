from __future__ import annotations
import logging
from datetime import datetime
from app.models.business import Business
from app.models.enums import BusinessStatus
from app.repositories.business import BusinessRepository
from app.utils.exceptions import NotFoundError

logger = logging.getLogger(__name__)

class BusinessService:
    def __init__(self, repo: BusinessRepository) -> None: self.repo = repo
    async def register(self, *, user_id, connection_id, telegram_user_id,
                       business_name=None, can_reply=True, rights=None) -> Business:
        existing = await self.repo.get_by_connection_id(connection_id)
        if existing:
            existing.status = BusinessStatus.CONNECTED
            existing.enabled = True
            existing.can_reply = can_reply
            existing.connected_at = datetime.utcnow()
            existing.disconnected_at = None
            existing.rights_data = rights
            existing.business_name = business_name or existing.business_name
            return existing
        biz = Business(user_id=user_id, business_connection_id=connection_id,
                       telegram_user_id=telegram_user_id, business_name=business_name,
                       can_reply=can_reply, status=BusinessStatus.CONNECTED, enabled=True,
                       rights_data=rights, connected_at=datetime.utcnow())
        return await self.repo.add(biz)
    async def toggle(self, business_id: int, enabled: bool) -> Business:
        biz = await self.repo.get(business_id)
        if not biz: raise NotFoundError("Business not found")
        biz.enabled = enabled; return biz
    async def disconnect(self, connection_id: str) -> None:
        biz = await self.repo.get_by_connection_id(connection_id)
        if biz: await self.repo.disconnect(biz.id)
