from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import async_session_factory
from app.config.settings import settings
from app.utils.security import decode_token

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

@router.get("/me")
async def me(user: dict = Depends(current_user)) -> dict:
    return {"ok": True, "data": user}

@router.get("/stats/global")
async def stats_global(_: dict = Depends(current_user), session: AsyncSession = Depends(get_session)) -> dict:
    from app.services import MessageService
    m = MessageService.__init__  # noqa
    from app.repositories import MessageRepository
    repo = MessageRepository(session)
    return {"ok": True, "data": await repo.stats()}
