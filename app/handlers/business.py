from __future__ import annotations
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.repositories.business import BusinessRepository

router = Router(name="business_h")

@router.callback_query(F.data == "biz:list")
async def list_businesses(call: CallbackQuery, session=None, db_user=None, **kwargs) -> None:
    repo = BusinessRepository(session)
    items = await repo.list_for_user(db_user.id)
    if not items:
        return await call.message.answer("Sizda ulangan Business hali yoq.\nTelegram sozlamalarida Business -> KRYZEN orqali ulang.")
    rows = []
    for b in items[:20]:
        status = "🟢" if b.status.value == "CONNECTED" and b.enabled else "🔴"
        rows.append(f"{status} <b>{b.business_name or b.business_connection_id[:8]}</b>  (#{b.id})")
    await call.message.answer("Biznesingiz:\n\n" + "\n".join(rows))
    await call.answer()
