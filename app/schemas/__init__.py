"""Pydantic schemas (DTOs)."""
from app.schemas.common import (
    BaseSchema,
    PaginationParams,
    PaginatedResponse,
    APIResponse,
)
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserOut,
    UserSettingsUpdate,
    UserStats,
)
from app.schemas.business import (
    BusinessCreate,
    BusinessOut,
    BusinessStats,
)
from app.schemas.message import (
    MessageOut,
    MessageStats,
    MessageSearch,
)
from app.schemas.rule import (
    RuleCreate,
    RuleUpdate,
    RuleOut,
    RuleTest,
)
from app.schemas.ai import (
    AISettings,
    AIRequest,
    AIResponse,
)
from app.schemas.promocode import (
    PromoCodeCreate,
    PromoCodeOut,
    PromoCodeRedeem,
)
from app.schemas.broadcast import (
    BroadcastRequest,
    BroadcastResult,
)
from app.schemas.auth import (
    TokenPayload,
    TokenResponse,
    LoginRequest,
)

__all__ = [
    "BaseSchema", "PaginationParams", "PaginatedResponse", "APIResponse",
    "UserCreate", "UserUpdate", "UserOut", "UserSettingsUpdate", "UserStats",
    "BusinessCreate", "BusinessOut", "BusinessStats",
    "MessageOut", "MessageStats", "MessageSearch",
    "RuleCreate", "RuleUpdate", "RuleOut", "RuleTest",
    "AISettings", "AIRequest", "AIResponse",
    "PromoCodeCreate", "PromoCodeOut", "PromoCodeRedeem",
    "BroadcastRequest", "BroadcastResult",
    "TokenPayload", "TokenResponse", "LoginRequest",
]
