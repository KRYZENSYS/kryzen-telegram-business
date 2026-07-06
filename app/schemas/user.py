"""User-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.schemas.common import BaseSchema


class UserCreate(BaseSchema):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None


class UserUpdate(BaseSchema):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_premium: bool | None = None
    premium_until: datetime | None = None


class UserSettingsUpdate(BaseSchema):
    ai_enabled: bool | None = None
    ai_model: str | None = None
    ai_temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    ai_top_p: float | None = Field(default=None, ge=0.0, le=1.0)
    ai_max_tokens: int | None = Field(default=None, ge=64, le=32_000)
    ai_system_prompt: str | None = None
    ai_memory_size: int | None = Field(default=None, ge=0, le=100)


class UserOut(BaseSchema):
    id: int
    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    role: str
    status: str
    is_premium: bool
    premium_until: datetime | None
    ai_enabled: bool
    ai_model: str | None
    created_at: datetime
    last_activity: datetime | None


class UserStats(BaseSchema):
    total: int
    active_today: int
    premium: int
    banned: int
    with_business: int
