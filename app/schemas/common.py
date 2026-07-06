"""Common schemas shared across the API."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Shared base schema config."""
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class PaginationParams(BaseModel):
    """Query-string pagination."""
    page: int = Field(default=1, ge=1, le=10_000)
    per_page: int = Field(default=20, ge=1, le=200)


class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response wrapper."""
    items: list[T]
    total: int
    page: int
    per_page: int
    pages: int

    @classmethod
    def build(cls, items: list[T], total: int, page: int, per_page: int) -> "PaginatedResponse[T]":
        pages = (total + per_page - 1) // per_page if per_page else 0
        return cls(items=items, total=total, page=page, per_page=per_page, pages=pages)


class APIResponse(BaseSchema, Generic[T]):
    """Standard API envelope."""
    success: bool = True
    data: T | None = None
    error: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IdResponse(BaseSchema):
    id: int


class DateRange(BaseModel):
    start: datetime | None = None
    end: datetime | None = None
