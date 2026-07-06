from __future__ import annotations
from typing import Generic, Type, TypeVar
from sqlalchemy import delete as sa_delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.base import Base
T = TypeVar("T", bound=Base)
class BaseRepository(Generic[T]):
    model: Type[T]
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def get(self, id: int) -> T | None: return await self.session.get(self.model, id)
    async def list_all(self, limit: int = 100, offset: int = 0) -> list[T]:
        r = await self.session.execute(select(self.model).limit(limit).offset(offset))
        return list(r.scalars().all())
    async def add(self, obj: T) -> T:
        self.session.add(obj); await self.session.flush(); return obj
    async def delete(self, id: int) -> bool:
        r = await self.session.execute(sa_delete(self.model).where(self.model.id == id))
        return r.rowcount > 0
