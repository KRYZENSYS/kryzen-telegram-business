"""Rule (auto-reply rule) model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import TimestampMixin
from app.models.enums import ReplyType, RuleSource, RuleType

if TYPE_CHECKING:
    from app.models.user import User


class Rule(Base, TimestampMixin):
    __tablename__ = "rules"
    __table_args__ = (Index("ix_rules_user_priority", "user_id", "priority", "is_active"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    rule_type: Mapped[RuleType] = mapped_column(
        SAEnum(RuleType, name="rule_type"), nullable=False
    )
    pattern: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[RuleSource] = mapped_column(
        SAEnum(RuleSource, name="rule_source"), default=RuleSource.AUTO_REPLY, nullable=False
    )

    reply_type: Mapped[ReplyType] = mapped_column(
        SAEnum(ReplyType, name="reply_type"), default=ReplyType.TEXT, nullable=False
    )
    reply_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    reply_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reply_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    random_replies: Mapped[list | None] = mapped_column(JSONB, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    delay_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    case_sensitive: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    match_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_matched_at: Mapped[str | None] = mapped_column(String(32), nullable=True)

    user: Mapped["User"] = relationship(lazy="joined")
