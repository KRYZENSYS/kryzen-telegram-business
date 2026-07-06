"""Media (photo, video, document, etc.) archived from Business messages."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Enum as SAEnum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import TimestampMixin
from app.models.enums import MediaType

if TYPE_CHECKING:
    from app.models.message import Message


class Media(Base, TimestampMixin):
    __tablename__ = "media"
    __table_args__ = (Index("ix_media_message_type", "message_id", "media_type"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    media_type: Mapped[MediaType] = mapped_column(
        SAEnum(MediaType, name="media_type"), nullable=False, index=True
    )
    file_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    file_unique_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    width: Mapped[int | None] = mapped_column(nullable=True)
    height: Mapped[int | None] = mapped_column(nullable=True)
    duration: Mapped[int | None] = mapped_column(nullable=True)
    thumbnail_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    local_path: Mapped[str | None] = mapped_column(String(512), nullable=True)

    message: Mapped["Message"] = relationship(back_populates="media", lazy="joined")
