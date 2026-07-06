#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from example, please fill BOT_TOKEN/SUPER_ADMIN_ID"; fi
docker compose up -d --build
docker compose logs -f api
