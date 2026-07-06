"""Generic async repository base class."""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Generic CRUD operations around an ORM model."""

    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, pk: int) -> T | None:
        return await self.session.get(self.model, pk)

    async def get_by(self, **filters: Any) -> T | None:
        stmt = select(self.model).filter_by(**filters).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        order_by: Any | None = None,
        offset: int = 0,
        limit: int = 100,
        **filters: Any,
    ) -> Sequence[T]:
        stmt = select(self.model).filter_by(**filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self, **filters: Any) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        return int((await self.session.execute(stmt)).scalar_one() or 0)

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def add_all(self, objs: list[T]) -> list[T]:
        self.session.add_all(objs)
        await self.session.flush()
        return objs

    async def update(self, obj: T, **fields: Any) -> T:
        for key, value in fields.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.flush()

    async def delete_by_id(self, pk: int) -> bool:
        result = await self.session.execute(delete(self.model).where(self.model.id == pk))
        return bool(result.rowcount)
