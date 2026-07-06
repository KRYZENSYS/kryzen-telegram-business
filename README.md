# KRYZEN Telegram Business

Production-grade multi-tenant **Telegram Business bot platform**: auto-replies, AI assistant, subscriptions, promo codes, Mini App dashboard, admin panel.

## Features

- Telegram Business connection lifecycle (connect / disconnect / enable / disable)
- AI assistant (OpenAI-compatible: Groq, OpenAI, OpenRouter) with per-user encrypted key + memory
- Smart auto-reply engine: 5 match types (EXACT, CONTAINS, STARTS_WITH, ENDS_WITH, REGEX)
- Random replies, delays, priority, case-sensitivity per rule
- Per-chat AI memory (last N messages)
- Promo codes (% discount, fixed discount, bonus days)
- Subscriptions (FREE / PREMIUM / BUSINESS)
- Telegram Mini App dashboard
- Full admin panel (broadcast, users, rules, analytics)
- Dockerized (api, bot, worker, postgres, redis, nginx)
- Type hints everywhere, mypy ready
- JWT auth + role enforcement
- Fernet at-rest encryption for secrets
- Throttling middleware
- Alembic migrations
- Pytest async suite
- GitHub Actions CI/CD

## Quick start

```bash
git clone https://github.com/KRYZENSYS/kryzen-telegram-business.git
cd kryzen-telegram-business
cp .env.example .env
# Edit .env: BOT_TOKEN, SUPER_ADMIN_ID
./scripts/start.sh
```

API: http://localhost:8000 | Docs: http://localhost:8000/api/docs

## License

MIT (c) KRYZEN
