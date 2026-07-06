from __future__ import annotations
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from app.services.promocode import PromoCodeService
from app.repositories.promocode import PromoCodeRepository
from app.services.subscription import SubscriptionService
from app.repositories.subscription import SubscriptionRepository
from app.repositories.user import UserRepository

router = Router(name="promo_h")

@router.callback_query(F.data == "promo:redeem")
async def prompt_redeem(call: CallbackQuery, **kwargs) -> None:
    await call.message.answer("Promo kodni yuboring (misol: <code>KRYZEN2026</code>):")
    await call.answer()

@router.message(Command("promo"))
async def cmd_promo(message: Message, session=None, db_user=None, **kwargs) -> None:
    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        return await message.answer("Foydalanish: /promo CODE")
    code = args[1].strip()
    repo = PromoCodeRepository(session)
    sub_svc = SubscriptionService(SubscriptionRepository(session), UserRepository(session))
    svc = PromoCodeService(repo, UserRepository(session), sub_svc)
    try:
        out = await svc.redeem(code=code, user_id=db_user.id)
        await message.answer(f"✅ Kod qabul qilindi! Bonus: {out['bonus_days']} kun")
    except Exception as e:
        await message.answer(f"❌ {e}")
