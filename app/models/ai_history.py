from __future__ import annotations
from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base, TimestampMixin

class AIHistory(Base, TimestampMixin):
    __tablename__ = "ai_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    model: Mapped[str | None] = mapped_column(String(64))
    prompt_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    extra_data: Mapped[dict | None] = mapped_column(JSON)
