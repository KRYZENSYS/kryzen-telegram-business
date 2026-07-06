"""Telegram Mini App initData signature verification.

Reference: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""
from __future__ import annotations

import hashlib
import hmac
import json
from collections import OrderedDict
from typing import Any
from urllib.parse import parse_qs

from app.config.settings import settings
from app.utils.exceptions import AuthenticationError


def parse_init_data(init_data: str) -> dict[str, str]:
    """Parse a raw initData query string into a flat dict."""
    parsed = parse_qs(init_data, keep_blank_values=True)
    return {k: v[0] for k, v in parsed.items()}


def verify_telegram_init_data(init_data: str, *, max_age_seconds: int = 86400) -> dict[str, Any]:
    """Verify a Mini App initData string and return the parsed user dict.

    Raises AuthenticationError on invalid or expired data.
    """
    if not init_data or "hash" not in init_data:
        raise AuthenticationError("Invalid initData: missing hash")

    data = parse_init_data(init_data)
    received_hash = data.pop("hash", "")

    # Build the data-check-string (sorted key=value pairs, newline-joined)
    check_pairs = OrderedDict(sorted(data.items()))
    data_check_string = "\n".join(f"{k}={v}" for k, v in check_pairs.items())

    secret_key = hmac.new(b"WebAppData", settings.bot_token.encode("utf-8"), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise AuthenticationError("Invalid initData signature")

    # Optional freshness check
    auth_date = int(data.get("auth_date", "0") or 0)
    if auth_date:
        import time
        if int(time.time()) - auth_date > max_age_seconds:
            raise AuthenticationError("initData expired")

    user_payload: dict[str, Any] = {}
    if "user" in data:
        try:
            user_payload = json.loads(data["user"])
        except json.JSONDecodeError as exc:
            raise AuthenticationError("Invalid user payload in initData") from exc

    return {"raw": data, "user": user_payload}
