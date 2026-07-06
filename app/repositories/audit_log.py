"""Audit log repository."""
from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import desc, func, select

from app.models.audit_log import AuditLog
from app.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    model = AuditLog

    async def list_recent(
        self,
        *,
        actor_id: int | None = None,
        target_user_id: int | None = None,
        action: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLog)
        if actor_id is not None:
            stmt = stmt.where(AuditLog.actor_id == actor_id)
        if target_user_id is not None:
            stmt = stmt.where(AuditLog.target_user_id == target_user_id)
        if action is not None:
            stmt = stmt.where(AuditLog.action == action)
        stmt = stmt.order_by(desc(AuditLog.created_at)).offset(offset).limit(limit)
        return (await self.session.execute(stmt)).scalars().all()

    async def count_since(self, since: datetime) -> int:
        stmt = select(func.count()).select_from(AuditLog).where(AuditLog.created_at >= since)
        return int((await self.session.execute(stmt)).scalar_one() or 0)
