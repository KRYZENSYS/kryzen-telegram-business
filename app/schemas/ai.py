"""AI schemas."""
from __future__ import annotations

from pydantic import Field

from app.schemas.common import BaseSchema


class AISettings(BaseSchema):
    api_key: str | None = None
    model: str = "llama-3.3-70b-versatile"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1024, ge=64, le=32_000)
    system_prompt: str | None = None
    memory_size: int = Field(default=10, ge=0, le=100)


class AIRequest(BaseSchema):
    chat_id: int
    message: str
    model: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    use_context: bool = True


class AIResponse(BaseSchema):
    reply: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    duration_ms: int
