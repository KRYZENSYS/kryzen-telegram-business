from __future__ import annotations
import logging, time
import httpx
from app.config.settings import settings
from app.models.ai_history import AIHistory
from app.repositories.ai_history import AIHistoryRepository
from app.services.user import UserService
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, history: AIHistoryRepository, users) -> None:
        self.history = history; self.users = users
    async def chat(self, *, user, chat_id: int, message: str, system=None,
                   model=None, temperature=None, max_tokens=None) -> dict:
        api_key = (self.users.get_api_key(user) if self.users else None) or settings.groq_api_key
        if not api_key: raise ValueError("No AI API key configured")
        base_url = settings.groq_base_url
        model_name = model or user.ai_model or settings.groq_default_model
        temp = temperature or user.ai_temperature or settings.ai_default_temperature
        max_t = max_tokens or user.ai_max_tokens or settings.ai_default_max_tokens
        sys_prompt = system or user.ai_system_prompt or "You are a helpful business assistant."
        memory = await self.history.recent(chat_id, limit=user.ai_memory_size or 10)
        messages = [{"role": "system", "content": sys_prompt}]
        for h in reversed(memory): messages.append({"role": h.role, "content": h.content})
        messages.append({"role": "user", "content": message})
        t0 = time.time()
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(f"{base_url}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model_name, "messages": messages, "temperature": temp, "max_tokens": max_t})
        dt = int((time.time() - t0) * 1000)
        r.raise_for_status()
        data = r.json()
        choice = data["choices"][0]["message"]
        usage = data.get("usage", {})
        await self.history.add(AIHistory(chat_id=chat_id, role="user", content=message, model=model_name,
            prompt_tokens=usage.get("prompt_tokens", 0), completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0), duration_ms=dt))
        await self.history.add(AIHistory(chat_id=chat_id, role="assistant", content=choice["content"], model=model_name,
            prompt_tokens=usage.get("prompt_tokens", 0), completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0), duration_ms=dt))
        return {"reply": choice["content"], "model": model_name, "usage": usage, "duration_ms": dt}
    async def clear_memory(self, chat_id: int) -> int: return await self.history.clear_for_chat(chat_id)
