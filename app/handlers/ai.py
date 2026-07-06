from __future__ import annotations
from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router(name="ai_h")

@router.callback_query(F.data == "ai:clear")
async def ai_clear(call: CallbackQuery, **kwargs) -> None:
    await call.message.answer("AI xotirasi tozalandi (joriy chat uchun).")
    await call.answer()
