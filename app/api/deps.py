from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.database.session import async_session_factory
from app.config.settings import settings
from app.utils.security import decode_token, create_access_token, verify_init_data
from app.repositories import UserRepository, MessageRepository, UserRepository
from app.services import UserService
from app.services import MessageService

async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

async def current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token, expected_type="access")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return {"id": int(payload["sub"]), "role": payload.get("role", "USER")}

router = APIRouter()

class TelegramAuthIn(BaseModel):
    init_data: str
    telegram_id: int
    first_name: str | None = None
    username: str | None = None

@router.post("/auth/telegram")
async def auth_telegram(body: TelegramAuthIn, session: AsyncSession = Depends(get_session)) -> dict:
    """Verify Telegram Mini App initData and return a JWT.
    On Replit the dev bot token is in settings.bot_token; signature is optional in dev mode.
    """
    try:
        if settings.bot_token:
            verify_init_data(body.init_data, bot_token=settings.bot_token)
    except ValueError:
        # In dev (no bot token) we accept the request without signature check
        if settings.bot_token:
            raise HTTPException(status_code=401, detail="Invalid initData signature")
    repo = UserRepository(session)
    svc = UserService(repo)
    user, _ = await svc.get_or_create(body.telegram_id, username=body.username, first_name=body.first_name)
    token = create_access_token(str(user.id), extra={"role": user.role.value})
    await session.commit()
    return {"ok": True, "data": {"access_token": token, "token_type": "Bearer", "user_id": user.id, "role": user.role.value}}

@router.get("/me")
async def me(user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)) -> dict:
    repo = UserRepository(session)
    u = await repo.get(user["id"])
    if not u: raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True, "data": {
        "id": u.id, "telegram_id": u.telegram_id, "username": u.username,
        "first_name": u.first_name, "last_name": u.last_name, "role": u.role.value,
        "is_premium": u.is_premium, "ai_enabled": u.ai_enabled, "ai_model": u.ai_model,
    }}

@router.get("/stats/global")
async def stats_global(_: dict = Depends(current_user), session: AsyncSession = Depends(get_session)) -> dict:
    m = MessageService(MessageRepository(session))
    return {"ok": True, "data": await m.stats()}

@router.get("/users/me")
async def users_me(user: dict = Depends(current_user)) -> dict:
    return {"ok": True, "data": user}
