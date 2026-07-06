from __future__ import annotations
import time
from collections import defaultdict
from typing import Any, Dict
from aiogram import BaseMiddleware

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit_per_minute: int = 30) -> None:
        self.window = 60.0; self.limit = rate_limit_per_minute
        self.calls: dict[int, list[float]] = defaultdict(list)
    async def __call__(self, handler, event, data: Dict[str, Any]) -> Any:
        u = data.get("event_from_user")
        if not u: return await handler(event, data)
        now = time.time(); q = self.calls[u.id]
        q[:] = [t for t in q if now - t < self.window]
        if len(q) >= self.limit: return None
        q.append(now)
        return await handler(event, data)
