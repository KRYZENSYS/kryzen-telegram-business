"""Promo code + redemption models."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class PromoCode(Base, TimestampMixin):
    __tablename__ = "promocodes"
    __table_args__ = (UniqueConstraint("code", name="uq_promocode_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)

    discount_percent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(default=0.0, nullable=False)
    bonus_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    max_uses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    used_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_per_user: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    redemptions: Mapped[list["PromoCodeRedemption"]] = relationship(
        back_populates="promocode", cascade="all, delete-orphan", lazy="selectin"
    )


class PromoCodeRedemption(Base):
    __tablename__ = "promo_redemptions"
    __table_args__ = (Index("ix_pr_user_code", "user_id", "promo_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    promo_id: Mapped[int] = mapped_column(
        ForeignKey("promocodes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    redeemed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    promocode: Mapped["PromoCode"] = relationship(back_populates="redemptions", lazy="joined")
