"""Message (incoming/outgoing Business chat message) model."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, Enum as SAEnum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import TimestampMixin
from app.models.enums import MessageDirection, MessageType

if TYPE_CHECKING:
    from app.models.chat import Chat
    from app.models.media import Media


class Message(Base, TimestampMixin):
    __tablename__ = "messages"
    __table_args__ = (
        Index("ix_messages_chat_created", "chat_id", "created_at"),
        Index("ix_messages_business_dir", "chat_id", "direction"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True
    )
    telegram_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    direction: Mapped[MessageDirection] = mapped_column(
        SAEnum(MessageDirection, name="message_direction"), nullable=False, index=True
    )
    message_type: Mapped[MessageType] = mapped_column(
        SAEnum(MessageType, name="message_type"), default=MessageType.TEXT, nullable=False
    )

    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)
    reply_to_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    edit_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    delete_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    extra_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    sender_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sender_username: Mapped[str | None] = mapped_column(String(64), nullable=True)

    matched_rule_id: Mapped[int | None] = mapped_column(nullable=True)
    ai_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    chat: Mapped["Chat"] = relationship(back_populates="messages", lazy="joined")
    media: Mapped[list["Media"]] = relationship(
        back_populates="message", cascade="all, delete-orphan", lazy="selectin"
    )
