from __future__ import annotations
from aiogram import Router
from aiogram.types import Message
from app.keyboards.menu import main_menu_kb

router = Router(name="fallback")

@router.message()
async def fallback(message: Message, db_user=None, **kwargs) -> None:
    await message.answer("Kerakli bolimni tanlang:", reply_markup=main_menu_kb(db_user.is_admin if db_user else False))
