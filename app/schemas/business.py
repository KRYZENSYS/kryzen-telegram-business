"""Business schemas."""
from __future__ import annotations

from datetime import datetime

from app.schemas.common import BaseSchema


class BusinessCreate(BaseSchema):
    business_connection_id: str
    telegram_user_id: int
    telegram_user_chat_id: int
    business_name: str | None = None
    can_reply: bool = True
    rights_data: dict | None = None


class BusinessOut(BaseSchema):
    id: int
    owner_id: int
    business_connection_id: str
    business_name: str | None
    telegram_user_id: int
    status: str
    enabled: bool
    connected_at: datetime
    disconnected_at: datetime | None
    chat_count: int = 0
    message_count: int = 0


class BusinessStats(BaseSchema):
    total: int
    connected: int
    disconnected: int
    total_messages: int
    total_media: int
