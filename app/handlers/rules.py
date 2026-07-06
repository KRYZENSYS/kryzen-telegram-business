from __future__ import annotations
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.repositories.rule import RuleRepository
from app.keyboards.menu import rules_list_kb

router = Router(name="rules_h")

@router.callback_query(F.data == "rules:list")
async def list_rules(call: CallbackQuery, session=None, db_user=None, **kwargs) -> None:
    repo = RuleRepository(session)
    rules = await repo.list_for_user(db_user.id)
    await call.message.answer(
        f"Sizda <b>{len(rules)}</b> ta qoida bor." if rules else "Qoidalar yoq. Yangi qoida qoshing.",
        reply_markup=rules_list_kb(rules) if rules else None,
    )
    await call.answer()
