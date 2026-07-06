from __future__ import annotations
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base, TimestampMixin
from app.models.enums import NotificationType

class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[NotificationType] = mapped_column(SAEnum(NotificationType, name="notification_type"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSON)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
