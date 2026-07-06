"""Symmetric encryption (Fernet) for sensitive values like Groq API keys."""
from __future__ import annotations

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from app.config.settings import settings
from app.utils.exceptions import KryzenError


def _key() -> bytes:
    """Derive a 32-byte Fernet key from settings.encryption_key."""
    raw = settings.encryption_key.encode("utf-8")
    if len(raw) >= 32:
        digest = hashlib.sha256(raw).digest()
    else:
        digest = raw.ljust(32, b"0")
    return base64.urlsafe_b64encode(digest)


def encrypt_value(plain: str | None) -> str | None:
    """Encrypt a string and return base64 ciphertext (or None)."""
    if plain is None or plain == "":
        return None
    try:
        return Fernet(_key()).encrypt(plain.encode("utf-8")).decode("ascii")
    except Exception as exc:  # noqa: BLE001
        raise KryzenError("Encryption failed") from exc


def decrypt_value(cipher: str | None) -> str | None:
    """Decrypt a value encrypted with `encrypt_value` (or None)."""
    if cipher is None or cipher == "":
        return None
    try:
        return Fernet(_key()).decrypt(cipher.encode("ascii")).decode("utf-8")
    except InvalidToken as exc:
        raise KryzenError("Invalid encryption token") from exc
