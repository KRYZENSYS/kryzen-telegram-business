"""Business repository."""
from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import func, select, update

from app.models.business import Business
from app.models.enums import BusinessStatus
from app.repositories.base import BaseRepository


class BusinessRepository(BaseRepository[Business]):
    model = Business

    async def get_by_connection_id(self, connection_id: str) -> Business | None:
        return await self.get_by(business_connection_id=connection_id)

    async def list_by_owner(self, owner_id: int) -> Sequence[Business]:
        stmt = select(Business).where(Business.owner_id == owner_id).order_by(Business.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_active(self) -> Sequence[Business]:
        stmt = select(Business).where(
            Business.status == BusinessStatus.CONNECTED, Business.enabled.is_(True)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def disconnect(self, business_id: int) -> None:
        await self.session.execute(
            update(Business)
            .where(Business.id == business_id)
            .values(status=BusinessStatus.DISCONNECTED, disconnected_at=datetime.utcnow(), enabled=False)
        )

    async def stats(self) -> dict[str, int]:
        total = await self.count()
        connected = await self.count(status=BusinessStatus.CONNECTED)
        disconnected = total - connected

        from app.models.media import Media
        from app.models.message import Message

        total_messages = int(
            (await self.session.execute(select(func.count()).select_from(Message))).scalar_one() or 0
        )
        total_media = int(
            (await self.session.execute(select(func.count()).select_from(Media))).scalar_one() or 0
        )
        return {
            "total": total,
            "connected": connected,
            "disconnected": disconnected,
            "total_messages": total_messages,
            "total_media": total_media,
        }
