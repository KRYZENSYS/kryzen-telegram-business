from __future__ import annotations
from datetime import datetime
from sqlalchemy import func, or_, select
from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    model = User
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        r = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return r.scalar_one_or_none()
    async def get_or_create(self, telegram_id: int, **kwargs) -> tuple[User, bool]:
        user = await self.get_by_telegram_id(telegram_id)
        if user: return user, False
        user = User(telegram_id=telegram_id, **kwargs)
        self.session.add(user); await self.session.flush()
        return user, True
    async def search(self, q: str = "", *, page: int = 1, page_size: int = 20) -> tuple[list[User], int]:
        stmt = select(User)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(or_(User.username.ilike(like), User.first_name.ilike(like),
                User.last_name.ilike(like), User.telegram_id.cast(__import__("sqlalchemy").String).ilike(like)))
        total = (await self.session.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
        r = await self.session.execute(stmt.order_by(User.id.desc()).limit(page_size).offset((page-1)*page_size))
        return list(r.scalars().all()), total
    async def touch_activity(self, user_id: int) -> None:
        await self.session.execute(User.__table__.update().where(User.id == user_id).values(last_activity=datetime.utcnow()))
