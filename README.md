# KRYZEN Telegram Business

Production-grade multi-tenant **Telegram Business bot platform** — optimized for Replit.

## Features

- Telegram Business connection lifecycle (connect / disconnect / enable / disable)
- AI assistant (OpenAI-compatible: Groq, OpenAI, OpenRouter) with per-user encrypted key + memory
- Smart auto-reply engine: 5 match types (EXACT, CONTAINS, STARTS_WITH, ENDS_WITH, REGEX)
- Random replies, delays, priority, case-sensitivity per rule
- Per-chat AI memory (last N messages)
- Promo codes (% discount, fixed discount, bonus days)
- Subscriptions (FREE / PREMIUM / BUSINESS)
- Full admin panel
- FastAPI dashboard API
- Type hints everywhere
- JWT auth + role enforcement
- Fernet at-rest encryption
- Throttling middleware

## Run on Replit

1. **Import this repo** to Replit (or fork).
2. **Add Secrets** (🔒 tab, NOT the .env file):
   - `BOT_TOKEN` — get from @BotFather
   - `SUPER_ADMIN_ID` — your Telegram numeric ID
   - `JWT_SECRET` — any long random string (e.g. `python -c "import secrets;print(secrets.token_urlsafe(48))"`)
   - `ENCRYPTION_KEY` — Fernet key: `python -c "from cryptography.fernet import Fernet;print(Fernet.generate_key().decode())"`
   - `GROQ_API_KEY` — (optional) for AI; get free at https://console.groq.com
3. **Click Run** — Replit installs deps and starts `main.py`.
4. Open the web tab — FastAPI at port 8080.

> Replit "Always On" is recommended for 24/7 uptime. Otherwise the bot sleeps when no one visits the web tab.

## Local quick start (optional)

```bash
pip install -r requirements.txt
export BOT_TOKEN=...
export SUPER_ADMIN_ID=...
python main.py
```

## Architecture (Replit-friendly)

- **One process**: `main.py` runs FastAPI + aiogram polling together (asyncio.gather).
- **SQLite** by default — no external DB needed. Switch to Postgres by setting `DATABASE_URL`.
- **Long polling** — no webhook URL required.
- **No Docker** — Replit's `replit.nix` provides Python 3.12 + sqlite + ffmpeg.

## Project layout

```
.
├── .replit                # Replit run config
├── replit.nix             # Replit Nix packages
├── main.py                # entry point: bot + API
├── app/
│   ├── api/               # FastAPI
│   ├── bot/               # aiogram bot
│   ├── business/          # Business connection dispatcher
│   ├── config/            # settings + logging
│   ├── database/          # async SQLAlchemy
│   ├── handlers/          # command/callback handlers
│   ├── middlewares/       # DB / user / throttling
│   ├── models/            # ORM models
│   ├── repositories/      # data access
│   ├── schemas/           # Pydantic IO
│   ├── services/          # business logic
│   ├── filters/           # role filters
│   ├── keyboards/         # inline keyboards
│   └── utils/             # security, exceptions
├── requirements.txt
├── .env.example
└── scripts/
```

## License

MIT (c) KRYZEN
