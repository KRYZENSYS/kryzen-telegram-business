#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
if [ ! -d .venv ]; then python3 -m venv .venv; fi
source .venv/bin/activate
pip install -q -r requirements.txt -r requirements-api.txt -r requirements-bot.txt
(uvicorn app.api.app:app --reload --port 8000 &)
(python -m app.bot.run &)
wait
