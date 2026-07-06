"""User repository."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import func, select, update

from app.models.enums import UserRole, UserStatus
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.get_by(telegram_id=telegram_id)

    async def get_or_create(
        self,
        telegram_id: int,
        *,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        language_code: str | None = None,
    ) -> tuple[User, bool]:
        existing = await self.get_by_telegram_id(telegram_id)
        if existing:
            return existing, False
        from app.config.settings import settings
        role = UserRole.USER
        if settings.super_admin_id and telegram_id == settings.super_admin_id:
            role = UserRole.SUPER_ADMIN
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
            role=role,
        )
        await self.add(user)
        return user, True

    async def set_premium(self, user_id: int, until: datetime | None) -> None:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_premium=until is not None and until > datetime.utcnow(), premium_until=until)
        )

    async def set_role(self, user_id: int, role: UserRole) -> None:
        await self.session.execute(update(User).where(User.id == user_id).values(role=role))

    async def set_status(self, user_id: int, status: UserStatus) -> None:
        await self.session.execute(update(User).where(User.id == user_id).values(status=status))

    async def touch_activity(self, telegram_id: int) -> None:
        await self.session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(last_activity=datetime.utcnow())
        )

    async def search(self, query: str, *, limit: int = 50) -> Sequence[User]:
        like = f"%{query.lower()}%"
        stmt = (
            select(User)
            .where(
                func.lower(func.coalesce(User.username, "")).like(like)
                | func.lower(func.coalesce(User.first_name, "")).like(like)
                | func.lower(func.coalesce(User.last_name, "")).like(like)
            )
            .order_by(User.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def stats(self) -> dict[str, int]:
        now = datetime.utcnow()
        today_start = datetime.combine(now.date(), datetime.min.time())

        total = await self.count()
        active_today = await self.count()
        premium = await self.count(is_premium=True)
        banned = await self.count(status=UserStatus.BANNED)

        from app.models.business import Business
        biz_stmt = select(func.count(func.distinct(Business.owner_id)))
        with_business = int((await self.session.execute(biz_stmt)).scalar_one() or 0)

        return {
            "total": total,
            "active_today": active_today,
            "premium": premium,
            "banned": banned,
            "with_business": with_business,
        }
