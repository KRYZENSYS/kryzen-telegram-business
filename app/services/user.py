from __future__ import annotations
import logging
from datetime import datetime, timedelta
from app.config.settings import settings
from app.models.enums import UserRole, UserStatus
from app.models.user import User
from app.repositories.user import UserRepository
from app.utils.security import decrypt_str, encrypt_str

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, repo: UserRepository) -> None: self.repo = repo
    async def get_or_create(self, telegram_id: int, **kwargs) -> tuple[User, bool]:
        user, created = await self.repo.get_or_create(telegram_id, **kwargs)
        if user.telegram_id == settings.super_admin_id and user.role != UserRole.SUPER_ADMIN:
            user.role = UserRole.SUPER_ADMIN
        return user, created
    async def ban(self, user_id: int) -> None:
        u = await self.repo.get(user_id)
        if u: u.status = UserStatus.BANNED
    async def unban(self, user_id: int) -> None:
        u = await self.repo.get(user_id)
        if u: u.status = UserStatus.ACTIVE
    async def set_premium(self, user_id: int, *, days: int) -> None:
        u = await self.repo.get(user_id)
        if not u: return
        u.is_premium = True
        base = u.premium_until or datetime.utcnow()
        u.premium_until = max(base, datetime.utcnow()) + timedelta(days=days)
    def set_api_key(self, user: User, key: str) -> None: user.ai_api_key_encrypted = encrypt_str(key)
    def get_api_key(self, user: User) -> str | None:
        if not user.ai_api_key_encrypted: return None
        try: return decrypt_str(user.ai_api_key_encrypted)
        except ValueError: return None
