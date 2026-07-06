"""Rule schemas."""
from __future__ import annotations

from pydantic import Field

from app.models.enums import ReplyType, RuleSource, RuleType
from app.schemas.common import BaseSchema


class RuleCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=128)
    rule_type: RuleType
    pattern: str = Field(min_length=1, max_length=4000)
    source: RuleSource = RuleSource.AUTO_REPLY
    reply_type: ReplyType = ReplyType.TEXT
    reply_text: str | None = None
    reply_file_id: str | None = None
    reply_metadata: dict | None = None
    random_replies: list[dict] | None = None
    priority: int = Field(default=10, ge=0, le=1000)
    delay_seconds: int = Field(default=0, ge=0, le=3600)
    case_sensitive: bool = False
    is_active: bool = True


class RuleUpdate(BaseSchema):
    name: str | None = None
    pattern: str | None = None
    reply_type: ReplyType | None = None
    reply_text: str | None = None
    reply_file_id: str | None = None
    reply_metadata: dict | None = None
    random_replies: list[dict] | None = None
    priority: int | None = None
    delay_seconds: int | None = None
    case_sensitive: bool | None = None
    is_active: bool | None = None


class RuleOut(BaseSchema):
    id: int
    user_id: int
    name: str
    rule_type: RuleType
    pattern: str
    source: RuleSource
    reply_type: ReplyType
    reply_text: str | None
    reply_file_id: str | None
    priority: int
    delay_seconds: int
    case_sensitive: bool
    is_active: bool
    match_count: int


class RuleTest(BaseSchema):
    text: str
    rule_id: int | None = None
