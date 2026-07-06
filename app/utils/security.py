from __future__ import annotations
import base64, hashlib, hmac, secrets, string
from datetime import datetime, timedelta
from typing import Any
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.config.settings import settings
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str: return pwd_ctx.hash(p)
def verify_password(p: str, h: str) -> bool:
    try: return pwd_ctx.verify(p, h)
    except Exception: return False

def _fernet():
    if not settings.encryption_key: return None
    try: return Fernet(settings.encryption_key.encode() if isinstance(settings.encryption_key, str) else settings.encryption_key)
    except Exception: return None
def encrypt_str(s: str) -> str:
    f = _fernet()
    if not f: return base64.b64encode(s.encode()).decode()
    return f.encrypt(s.encode()).decode()
def decrypt_str(s: str) -> str:
    f = _fernet()
    if not f: return base64.b64decode(s.encode()).decode().decode()
    return f.decrypt(s.encode()).decode()

def _now(): return datetime.utcnow()
def create_access_token(sub: str, extra=None) -> str:
    p = {"sub": sub, "type": "access", "iat": int(_now().timestamp()), "exp": int((_now() + timedelta(minutes=settings.access_token_expire_minutes)).timestamp())}
    if extra: p.update(extra)
    return jwt.encode(p, settings.jwt_secret, algorithm=settings.jwt_algorithm)
def create_refresh_token(sub: str) -> str:
    p = {"sub": sub, "type": "refresh", "iat": int(_now().timestamp()), "exp": int((_now() + timedelta(days=settings.refresh_token_expire_days)).timestamp())}
    return jwt.encode(p, settings.jwt_secret, algorithm=settings.jwt_algorithm)
def decode_token(token: str, *, expected_type="access") -> dict:
    try: payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as e: raise ValueError(str(e))
    if payload.get("type") != expected_type: raise ValueError("Wrong token type")
    return payload

def generate_promo_code(length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
def hash_sha256(s: str) -> str: return hashlib.sha256(s.encode()).hexdigest()
def verify_init_data(init_data: str, *, bot_token: str) -> dict:
    fields = {}
    for p in init_data.split("&"):
        if "=" in p: k, v = p.split("=", 1); fields[k] = v
    rh = fields.pop("hash", "")
    dcs = "\\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
    secret = hashlib.sha256(bot_token.encode()).digest()
    if not hmac.compare_digest(hmac.new(secret, dcs.encode(), hashlib.sha256).hexdigest(), rh):
        raise ValueError("Invalid initData signature")
    return fields
