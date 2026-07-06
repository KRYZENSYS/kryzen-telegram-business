from __future__ import annotations
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.filters.role import AdminFilter
from app.services import MessageService
from app.repositories import MessageRepository, UserRepository

router = Router(name="admin_h")
router.callback_query.filter(AdminFilter())

@router.callback_query(F.data == "admin:panel")
async def admin_panel(call: CallbackQuery, session=None, **kwargs) -> None:
    m = MessageService(MessageRepository(session))
    msg_stats = await m.stats()
    users_total = len(await UserRepository(session).list_all(limit=1000))
    await call.message.answer(
        "<b>Admin panel</b>\n\n"
        f"Users: <b>{users_total}</b>\n"
        f"Messages: total={msg_stats['total']}, in={msg_stats['incoming']}, out={msg_stats['outgoing']}"
    )
    await call.answer()
