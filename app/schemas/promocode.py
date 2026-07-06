"""Promo code schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.schemas.common import BaseSchema


class PromoCodeCreate(BaseSchema):
    code: str = Field(min_length=3, max_length=64)
    description: str | None = None
    discount_percent: int = Field(default=0, ge=0, le=100)
    discount_amount: float = Field(default=0.0, ge=0)
    bonus_days: int = Field(default=0, ge=0, le=3650)
    max_uses: int = Field(default=0, ge=0)
    max_per_user: int = Field(default=1, ge=1)
    starts_at: datetime | None = None
    expires_at: datetime | None = None
    is_active: bool = True


class PromoCodeOut(BaseSchema):
    id: int
    code: str
    description: str | None
    discount_percent: int
    discount_amount: float
    bonus_days: int
    max_uses: int
    used_count: int
    max_per_user: int
    starts_at: datetime | None
    expires_at: datetime | None
    is_active: bool
    created_at: datetime


class PromoCodeRedeem(BaseSchema):
    code: str
