"""Time helpers (timezone-aware UTC, formatting, parsing)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def utcnow() -> datetime:
    """Timezone-aware current UTC datetime."""
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)


def format_dt(dt: datetime | None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not dt:
        return "—"
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt.strftime(fmt)


def parse_dt(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None) if value.tzinfo else value
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%d.%m.%Y %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None
