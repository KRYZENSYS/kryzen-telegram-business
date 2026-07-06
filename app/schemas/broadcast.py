"""Broadcast schemas."""
from __future__ import annotations

from pydantic import Field

from app.schemas.common import BaseSchema


class BroadcastRequest(BaseSchema):
    text: str | None = None
    photo: str | None = None
    video: str | None = None
    document: str | None = None
    voice: str | None = None
    animation: str | None = None
    sticker: str | None = None
    parse_mode: str | None = None
    target_premium_only: bool = False
    target_status: str = "active"


class BroadcastResult(BaseSchema):
    total: int
    sent: int
    failed: int
    duration_seconds: float
    errors: list[str] = Field(default_factory=list)
