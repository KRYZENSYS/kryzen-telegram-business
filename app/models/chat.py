from __future__ import annotations
from sqlalchemy import Integer, BigInteger, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

class Chat(Base, TimestampMixin):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    business_id: Mapped[int] = mapped_column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    chat_type: Mapped[str] = mapped_column(String(16), nullable=False, default="private")
    title: Mapped[str | None] = mapped_column(String(255))
    username: Mapped[str | None] = mapped_column(String(64))
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ai_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    business: Mapped["Business"] = relationship("Business", back_populates="chats")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
