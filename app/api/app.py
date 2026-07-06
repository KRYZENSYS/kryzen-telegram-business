from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from app.config.settings import settings
from app.api.deps import router as api_router
from app.database.session import async_session_factory
from app.database.base import Base
import app.models._registry  # noqa: F401

app = FastAPI(title="KRYZEN Telegram Business API", version="1.0.0")

origins = [o.strip() for o in settings.cors_origins.split(",")] if settings.cors_origins else ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
async def _on_startup() -> None:
    async with async_session_factory().bind.begin() as _:
        # For development; in production prefer alembic upgrade head
        if settings.database_url.startswith("sqlite"):
            async with async_session_factory() as s:
                await s.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health() -> dict: return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")
