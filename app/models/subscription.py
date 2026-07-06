from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, Float, String, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin
from app.models.enums import SubscriptionPlan, SubscriptionStatus

class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan: Mapped[SubscriptionPlan] = mapped_column(SAEnum(SubscriptionPlan, name="subscription_plan"), nullable=False)
    status: Mapped[SubscriptionStatus] = mapped_column(SAEnum(SubscriptionStatus, name="subscription_status"), nullable=False, default=SubscriptionStatus.ACTIVE)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    promo_code: Mapped[str | None] = mapped_column(String(64))
    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    auto_renew: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")
