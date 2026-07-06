from __future__ import annotations
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.keyboards.menu import main_menu_kb

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: Message, db_user=None, **kwargs) -> None:
    text = (
        f"Salom, <b>{db_user.full_name}</b>!\n\n"
        "Men KRYZEN — sizning Telegram Business yordamchingizman.\n"
        "Avtomatik javoblar, AI yordamchi va boshqalar."
    )
    await message.answer(text, reply_markup=main_menu_kb(db_user.is_admin if db_user else False))
