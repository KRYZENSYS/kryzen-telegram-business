"""JWT token issuance and validation."""
from __future__ import annotations

import base64
import hashlib
import hmac
import time
from typing import Any

import jwt

from app.config.settings import settings
from app.utils.exceptions import AuthenticationError


def create_access_token(
    subject: str | int,
    *,
    extra_claims: dict[str, Any] | None = None,
    expires_in: int | None = None,
) -> str:
    """Create a short-lived access token."""
    now = int(time.time())
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": now + (expires_in or settings.jwt_access_ttl),
        "type": "access",
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str | int) -> str:
    """Create a long-lived refresh token."""
    now = int(time.time())
    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": now + settings.jwt_refresh_ttl,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str, *, expected_type: str | None = None) -> dict[str, Any]:
    """Decode and validate a JWT. Raises AuthenticationError on failure."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["sub", "exp", "iat"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise AuthenticationError("Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise AuthenticationError(f"Invalid token: {exc}") from exc

    if expected_type and payload.get("type") != expected_type:
        raise AuthenticationError(f"Expected {expected_type} token")

    return payload


def hash_token(token: str) -> str:
    """Return a short SHA-256 fingerprint of a token (for revocation lists)."""
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
