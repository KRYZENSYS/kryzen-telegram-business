"""Auth schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.schemas.common import BaseSchema


class LoginRequest(BaseSchema):
    init_data: str = Field(min_length=10, description="Telegram Mini App initData string")


class TokenPayload(BaseSchema):
    sub: str
    user_id: int
    role: str
    iat: datetime | None = None
    exp: datetime | None = None


class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
