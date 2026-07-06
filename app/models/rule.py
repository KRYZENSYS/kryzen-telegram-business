from __future__ import annotations
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin
from app.models.enums import RuleType, RuleSource, ReplyType

class Rule(Base, TimestampMixin):
    __tablename__ = "rules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    rule_type: Mapped[RuleType] = mapped_column(SAEnum(RuleType, name="rule_type"), nullable=False)
    pattern: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[RuleSource] = mapped_column(SAEnum(RuleSource, name="rule_source"), nullable=False, default=RuleSource.AUTO_REPLY)
    reply_type: Mapped[ReplyType] = mapped_column(SAEnum(ReplyType, name="reply_type"), nullable=False, default=ReplyType.TEXT)
    reply_text: Mapped[str | None] = mapped_column(Text)
    reply_file_id: Mapped[str | None] = mapped_column(String(255))
    reply_metadata: Mapped[dict | None] = mapped_column(JSON)
    random_replies: Mapped[list | None] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    delay_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    case_sensitive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    match_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_matched_at: Mapped[str | None] = mapped_column(String(32))
    user: Mapped["User"] = relationship("User", back_populates="rules")
