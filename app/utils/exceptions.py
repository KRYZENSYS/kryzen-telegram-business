"""Custom exception hierarchy."""
from __future__ import annotations


class KryzenError(Exception):
    """Base error for KRYZEN platform."""
    status_code: int = 500
    message: str = "Internal error"

    def __init__(self, message: str | None = None, *, status_code: int | None = None) -> None:
        super().__init__(message or self.message)
        self.message = message or self.message
        if status_code is not None:
            self.status_code = status_code


class NotFoundError(KryzenError):
    status_code = 404
    message = "Resource not found"


class AlreadyExistsError(KryzenError):
    status_code = 409
    message = "Resource already exists"


class ValidationError(KryzenError):
    status_code = 422
    message = "Validation failed"


class PermissionDeniedError(KryzenError):
    status_code = 403
    message = "Permission denied"


class AuthenticationError(KryzenError):
    status_code = 401
    message = "Authentication required"


class RateLimitError(KryzenError):
    status_code = 429
    message = "Rate limit exceeded"


class BusinessAPIError(KryzenError):
    status_code = 502
    message = "Telegram Business API error"


class AIProviderError(KryzenError):
    status_code = 502
    message = "AI provider error"


class PremiumRequiredError(KryzenError):
    status_code = 402
    message = "Premium subscription required"


__all__ = [
    "KryzenError", "NotFoundError", "AlreadyExistsError", "ValidationError",
    "PermissionDeniedError", "AuthenticationError", "RateLimitError",
    "BusinessAPIError", "AIProviderError", "PremiumRequiredError",
]
