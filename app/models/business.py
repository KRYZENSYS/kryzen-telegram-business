from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, BigInteger, Boolean, String, DateTime, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin
from app.models.enums import BusinessStatus

class Business(Base, TimestampMixin):
    __tablename__ = "businesses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    business_connection_id: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    business_name: Mapped[str | None] = mapped_column(String(255))
    can_reply: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    status: Mapped[BusinessStatus] = mapped_column(SAEnum(BusinessStatus, name="business_status"), nullable=False, default=BusinessStatus.DISCONNECTED)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    rights_data: Mapped[dict | None] = mapped_column(JSON)
    connected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    disconnected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user: Mapped["User"] = relationship("User", back_populates="businesses")
    chats: Mapped[list["Chat"]] = relationship("Chat", back_populates="business", cascade="all, delete-orphan")
