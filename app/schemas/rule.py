from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class RuleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    rule_type: str; pattern: str = Field(..., min_length=1)
    source: str = "AUTO_REPLY"; reply_type: str = "TEXT"
    reply_text: str | None = None; reply_file_id: str | None = None; random_replies: list[dict] | None = None
    is_active: bool = True; priority: int = Field(default=10, ge=0, le=1000)
    delay_seconds: int = Field(default=0, ge=0, le=60); case_sensitive: bool = False
class RuleCreate(RuleBase): pass
class RuleUpdate(BaseModel):
    name: str | None = None; pattern: str | None = None; reply_type: str | None = None
    reply_text: str | None = None; reply_file_id: str | None = None; random_replies: list[dict] | None = None
    is_active: bool | None = None; priority: int | None = None
    delay_seconds: int | None = None; case_sensitive: bool | None = None
class RuleOut(RuleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int; match_count: int; created_at: datetime
