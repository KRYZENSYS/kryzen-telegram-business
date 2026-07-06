from __future__ import annotations
from aiogram.filters import BaseFilter
from app.models.enums import UserRole

class RoleFilter(BaseFilter):
    def __init__(self, *roles: UserRole) -> None: self.roles = roles
    async def __call__(self, message, db_user=None, **kwargs) -> bool:
        return bool(db_user and db_user.role in self.roles)

class AdminFilter(RoleFilter):
    def __init__(self) -> None: super().__init__(UserRole.ADMIN, UserRole.SUPER_ADMIN)
class SuperAdminFilter(RoleFilter):
    def __init__(self) -> None: super().__init__(UserRole.SUPER_ADMIN)
