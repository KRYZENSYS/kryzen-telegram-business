"""Input validation utilities."""
from __future__ import annotations

import re

from app.config.logging import logger

TELEGRAM_ID_RE = re.compile(r"^\d{5,15}$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{5,32}$")
PROMO_CODE_RE = re.compile(r"^[A-Z0-9_-]{3,64}$")


def is_valid_regex(pattern: str) -> bool:
    try:
        re.compile(pattern)
        return True
    except re.error as exc:
        logger.debug("Invalid regex: {} - {}", pattern, exc)
        return False


def validate_telegram_id(value: object) -> bool:
    return bool(TELEGRAM_ID_RE.match(str(value)))


def validate_username(value: object) -> bool:
    return bool(USERNAME_RE.match(str(value or "").lstrip("@")))


def validate_promo_code(value: object) -> bool:
    return bool(PROMO_CODE_RE.match(str(value or "").upper()))
