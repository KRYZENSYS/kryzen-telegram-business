"""Generic helper utilities (string, number, formatting)."""
from __future__ import annotations

import html
import re
import secrets
import string
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def generate_id(length: int = 12, alphabet: str = string.ascii_letters + string.digits) -> str:
    """Return a secure random identifier."""
    return "".join(secrets.choice(alphabet) for _ in range(length))


def mask_string(value: str | None, visible: int = 4) -> str:
    """Mask a string keeping the first/last `visible` chars (e.g. tokens)."""
    if not value:
        return ""
    if len(value) <= visible * 2:
        return "*" * len(value)
    return f"{value[:visible]}{'*' * (len(value) - visible * 2)}{value[-visible:]}"


def truncate(text: str | None, limit: int = 256, suffix: str = "…") -> str:
    if not text:
        return ""
    return text if len(text) <= limit else text[: limit - len(suffix)] + suffix


def format_bytes(size: int | None) -> str:
    if size is None:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    n = float(size)
    for unit in units:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def format_duration(seconds: int | float) -> str:
    seconds = int(seconds)
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    if days:
        return f"{days}d {hours}h {minutes}m"
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


def escape_html(text: str | None) -> str:
    return html.escape(text or "", quote=True)


def safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def chunked(items: Iterable[T], size: int) -> Iterable[list[T]]:
    """Split an iterable into lists of length `size`."""
    chunk: list[T] = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
