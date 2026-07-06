from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, BigInteger, String, Text, Boolean, DateTime, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin
from app.models.enums import MessageDirection, MessageType

class Message(Base, TimestampMixin):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    telegram_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    direction: Mapped[MessageDirection] = mapped_column(SAEnum(MessageDirection, name="message_direction"), nullable=False)
    message_type: Mapped[MessageType] = mapped_column(SAEnum(MessageType, name="message_type"), nullable=False, default=MessageType.TEXT)
    text: Mapped[str | None] = mapped_column(Text)
    caption: Mapped[str | None] = mapped_column(Text)
    reply_to_message_id: Mapped[int | None] = mapped_column(BigInteger)
    is_edited: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    edit_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    delete_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    extra_data: Mapped[dict | None] = mapped_column(JSON)
    sender_name: Mapped[str | None] = mapped_column(String(255))
    sender_username: Mapped[str | None] = mapped_column(String(64))
    matched_rule_id: Mapped[int | None] = mapped_column(Integer)
    ai_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
