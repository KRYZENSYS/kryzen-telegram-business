from __future__ import annotations
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.menu import main_menu_kb, ai_menu_kb

router = Router(name="menu")

@router.callback_query(F.data == "menu:main")
async def back_to_main(call: CallbackQuery, db_user=None, **kwargs) -> None:
    await call.message.answer("Asosiy menyu:", reply_markup=main_menu_kb(db_user.is_admin if db_user else False))
    await call.answer()

@router.callback_query(F.data == "ai:menu")
async def ai_menu(call: CallbackQuery, **kwargs) -> None:
    await call.message.answer("AI sozlamalari:", reply_markup=ai_menu_kb())
    await call.answer()

@router.callback_query(F.data == "stats:me")
async def stats(call: CallbackQuery, db_user=None, **kwargs) -> None:
    await call.message.answer(
        f"<b>Statistika:</b>\n"
        f"ID: <code>{db_user.id}</code>\n"
        f"Role: {db_user.role.value}\n"
        f"Premium: {'ha' if db_user.is_premium else 'yoq'}"
    )
    await call.answer()
