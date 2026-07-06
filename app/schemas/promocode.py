from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class PromoCodeBase(BaseModel):
    code: str = Field(..., min_length=3, max_length=64); description: str | None = None
    discount_percent: int = Field(default=0, ge=0, le=100)
    discount_amount: float = Field(default=0.0, ge=0)
    bonus_days: int = Field(default=0, ge=0, le=3650)
    max_uses: int = Field(default=0, ge=0); max_per_user: int = Field(default=1, ge=1)
    starts_at: datetime | None = None; expires_at: datetime | None = None; is_active: bool = True
class PromoCodeCreate(PromoCodeBase): pass
class PromoCodeUpdate(BaseModel):
    description: str | None = None; discount_percent: int | None = None
    discount_amount: float | None = None; bonus_days: int | None = None
    max_uses: int | None = None; max_per_user: int | None = None
    starts_at: datetime | None = None; expires_at: datetime | None = None; is_active: bool | None = None
class PromoCodeOut(PromoCodeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int; used_count: int; created_at: datetime
class RedeemIn(BaseModel): code: str
class RedeemOut(BaseModel):
    code: str; bonus_days: int; discount_percent: int; discount_amount: float
