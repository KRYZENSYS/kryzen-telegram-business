"""Message schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.schemas.common import BaseSchema, PaginationParams


class MessageOut(BaseSchema):
    id: int
    chat_id: int
    telegram_message_id: int
    direction: str
    message_type: str
    text: str | None
    caption: str | None
    is_edited: bool
    is_deleted: bool
    edit_date: datetime | None
    sender_name: str | None
    ai_used: bool
    created_at: datetime


class MessageSearch(PaginationParams):
    chat_id: int | None = None
    direction: str | None = None
    message_type: str | None = None
    text_query: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None


class MessageStats(BaseSchema):
    total: int
    incoming: int
    outgoing: int
    by_type: dict[str, int] = Field(default_factory=dict)
    today: int
    this_week: int
    this_month: int
