from __future__ import annotations
from pydantic import BaseModel, Field
class AISettings(BaseModel):
    enabled: bool = True; api_key: str | None = None; model: str | None = None
    temperature: float | None = Field(default=None, ge=0, le=2)
    top_p: float | None = Field(default=None, ge=0, le=1)
    max_tokens: int | None = Field(default=None, ge=1, le=32000)
    system_prompt: str | None = None
    memory_size: int | None = Field(default=None, ge=1, le=100)
class AIChatIn(BaseModel):
    chat_id: int; message: str = Field(..., min_length=1, max_length=8000)
    system: str | None = None; model: str | None = None
    temperature: float | None = None; max_tokens: int | None = None
class AIChatOut(BaseModel):
    reply: str; model: str; usage: dict; duration_ms: int
