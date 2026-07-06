from __future__ import annotations
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.config.settings import settings
from app.api.deps import router as api_router
from app.database.session import async_session_factory
from app.database.base import Base
import app.models._registry  # noqa: F401

app = FastAPI(title="KRYZEN Telegram Business API", version="1.0.0")

origins = [o.strip() for o in settings.cors_origins.split(",")] if settings.cors_origins else ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Static + templates
BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
static_dir = os.path.join(BASE, "app", "static")
templates_dir = os.path.join(BASE, "app", "templates")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>KRYZEN Telegram Business</title>
<style>
  :root { --bg:#0b0d10; --fg:#e8eef3; --accent:#7c5cff; --muted:#8a96a3; }
  * { box-sizing: border-box; }
  body { margin:0; font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; background: radial-gradient(1200px 600px at 10% -10%, #1a1d27 0%, transparent 60%), radial-gradient(900px 500px at 110% 10%, #2a1f4a 0%, transparent 60%), var(--bg); color: var(--fg); min-height: 100vh; }
  .wrap { max-width: 960px; margin: 0 auto; padding: 48px 24px; }
  h1 { font-size: 44px; margin: 0 0 8px; letter-spacing: -0.02em; }
  .sub { color: var(--muted); margin-bottom: 32px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
  .card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; backdrop-filter: blur(8px); }
  .card h3 { margin: 0 0 6px; font-size: 18px; }
  .card p { margin: 0; color: var(--muted); font-size: 14px; line-height: 1.5; }
  .pill { display: inline-block; padding: 4px 10px; border-radius: 999px; background: rgba(124,92,255,0.18); color: #c2b0ff; font-size: 12px; }
  a { color: #c2b0ff; }
  .endpoints a { display: block; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }
</style>
</head>
<body>
<div class="wrap">
  <span class="pill">KRYZEN</span>
  <h1>Telegram Business Bot</h1>
  <p class="sub">Auto-replies, AI assistant, subscriptions, promo codes — running on Replit.</p>
  <div class="grid">
    <div class="card"><h3>🤖 Bot</h3><p>Send /start to your Telegram bot to open the user dashboard.</p></div>
    <div class="card"><h3>🧠 AI</h3><p>Per-user encrypted OpenAI-compatible key, 10-message memory, 5 model providers.</p></div>
    <div class="card"><h3>🎁 Promo</h3><p>Discount codes, bonus days, plan upgrades.</p></div>
    <div class="card"><h3>⚙️ Auto-reply</h3><p>5 match types, random replies, priorities, delays, case-sensitivity.</p></div>
  </div>
  <h2 style="margin-top:40px">API endpoints</h2>
  <div class="card endpoints">
    <a href="/health">/health</a>
    <a href="/api/docs">/api/docs</a>
    <a href="/api/redoc">/api/redoc</a>
    <a href="/api/v1/me">/api/v1/me (requires Bearer JWT)</a>
    <a href="/api/v1/stats/global">/api/v1/stats/global (requires Bearer JWT)</a>
  </div>
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)

@app.get("/health")
async def health() -> dict: return {"status": "ok", "service": "kryzen-telegram-business"}

app.include_router(api_router, prefix="/api/v1")
