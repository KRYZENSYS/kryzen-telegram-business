from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; telegram_id: int
    username: str | None = None; first_name: str | None = None; last_name: str | None = None
    language_code: str | None = None; role: str; status: str
    is_premium: bool; premium_until: datetime | None = None
    ai_enabled: bool; ai_model: str | None = None; created_at: datetime
class UserUpdate(BaseModel):
    first_name: str | None = None; last_name: str | None = None; language_code: str | None = None
    ai_enabled: bool | None = None; ai_model: str | None = None
    ai_temperature: float | None = Field(default=None, ge=0, le=2)
    ai_top_p: float | None = Field(default=None, ge=0, le=1)
    ai_max_tokens: int | None = Field(default=None, ge=1, le=32000)
    ai_system_prompt: str | None = None
    ai_memory_size: int | None = Field(default=None, ge=1, le=100)
