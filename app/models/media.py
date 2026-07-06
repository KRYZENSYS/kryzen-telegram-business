from __future__ import annotations
from sqlalchemy import Integer, BigInteger, String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base, TimestampMixin
from app.models.enums import MediaType

class Media(Base, TimestampMixin):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, index=True)
    media_type: Mapped[MediaType] = mapped_column(SAEnum(MediaType, name="media_type"), nullable=False)
    file_id: Mapped[str | None] = mapped_column(String(255), index=True)
    file_unique_id: Mapped[str | None] = mapped_column(String(128), index=True)
    file_name: Mapped[str | None] = mapped_column(String(255))
    mime_type: Mapped[str | None] = mapped_column(String(128))
    file_size: Mapped[int | None] = mapped_column(BigInteger)
    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)
    duration: Mapped[int | None] = mapped_column(Integer)
    thumbnail_file_id: Mapped[str | None] = mapped_column(String(255))
    local_path: Mapped[str | None] = mapped_column(String(512))
