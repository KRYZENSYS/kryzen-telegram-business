from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Integer, BigInteger, Boolean, Float, DateTime, Enum as SAEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin
from app.models.enums import UserRole, UserStatus

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(64))
    first_name: Mapped[str | None] = mapped_column(String(128))
    last_name: Mapped[str | None] = mapped_column(String(128))
    language_code: Mapped[str | None] = mapped_column(String(8), default="en")
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole, name="user_role"), nullable=False, default=UserRole.USER)
    status: Mapped[UserStatus] = mapped_column(SAEnum(UserStatus, name="user_status"), nullable=False, default=UserStatus.ACTIVE)
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    premium_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ai_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    ai_model: Mapped[str | None] = mapped_column(String(64))
    ai_temperature: Mapped[float | None] = mapped_column(Float)
    ai_top_p: Mapped[float | None] = mapped_column(Float)
    ai_max_tokens: Mapped[int | None] = mapped_column(Integer)
    ai_system_prompt: Mapped[str | None] = mapped_column(Text)
    ai_memory_size: Mapped[int | None] = mapped_column(Integer, default=10)
    ai_api_key_encrypted: Mapped[str | None] = mapped_column(Text)
    last_activity: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    businesses: Mapped[list["Business"]] = relationship("Business", back_populates="user", cascade="all, delete-orphan")
    rules: Mapped[list["Rule"]] = relationship("Rule", back_populates="user", cascade="all, delete-orphan")
    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    @property
    def is_admin(self) -> bool: return self.role in (UserRole.ADMIN, UserRole.SUPER_ADMIN)
    @property
    def full_name(self) -> str:
        parts = [self.first_name or "", self.last_name or ""]
        return " ".join(p for p in parts if p) or self.username or f"user_{self.telegram_id}"
