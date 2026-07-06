from __future__ import annotations
import asyncio, logging
from datetime import datetime
from sqlalchemy import select, update
from aiogram.types import BusinessConnection, BusinessMessagesDeleted, Message
from app.models.enums import BusinessStatus, MessageDirection, MessageType
from app.models.message import Message as MessageModel
from app.models.chat import Chat as ChatModel
from app.services import BusinessService, MessageService, RuleService, AIService
from app.repositories import BusinessRepository, ChatRepository, MessageRepository, RuleRepository, AIHistoryRepository
from app.services.user import UserService
from app.repositories.user import UserRepository
logger = logging.getLogger(__name__)

def _map_message_type(m):
    if m.photo: return MessageType.PHOTO
    if m.video: return MessageType.VIDEO
    if m.document: return MessageType.DOCUMENT
    if m.voice: return MessageType.VOICE
    if m.audio: return MessageType.AUDIO
    if m.sticker: return MessageType.STICKER
    if m.animation: return MessageType.ANIMATION
    return MessageType.TEXT

class BusinessEventDispatcher:
    async def on_connection(self, event, *, session, **_):
        bizs = BusinessRepository(session)
        users = UserRepository(session)
        svc = BusinessService(bizs)
        owner = await users.get_by_telegram_id(event.user_chat_id) if event.user_chat_id else None
        if not owner:
            logger.warning("Business connection for unknown user_chat_id=%s", event.user_chat_id); return
        if event.is_enabled:
            await svc.register(user_id=owner.id, connection_id=event.id,
                telegram_user_id=event.user_chat_id, business_name=event.name,
                can_reply=getattr(event, "can_reply", True), rights=None)
        else:
            await svc.disconnect(event.id)
        await session.commit()

    async def on_message(self, message, *, session, bot=None, **_):
        bizs = BusinessRepository(session)
        chats = ChatRepository(session)
        msgs = MessageRepository(session)
        biz = await bizs.get_by_connection_id(message.business_connection_id)
        if not biz or not biz.enabled: return
        chat, _ = await chats.get_or_create(business_id=biz.id, telegram_chat_id=message.chat.id, chat_type=message.chat.type)
        await MessageService(msgs).save(chat_id=chat.id, telegram_message_id=message.message_id,
            direction=MessageDirection.INCOMING, message_type=_map_message_type(message),
            text=message.text, caption=message.caption,
            sender_name=message.from_user.full_name if message.from_user else None,
            sender_username=message.from_user.username if message.from_user else None,
            reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None)
        if not message.text or not biz.can_reply: return
        rules = await RuleRepository(session).list_active_for_user(biz.user_id)
        rule = RuleService().find_match(rules, message.text)
        if rule:
            await RuleService().bump_match(rule.id)
            await MessageService(msgs).save(chat_id=chat.id, telegram_message_id=0,
                direction=MessageDirection.OUTGOING, message_type=MessageType.TEXT,
                text=rule.reply_text, matched_rule_id=rule.id)
            if rule.delay_seconds: await asyncio.sleep(rule.delay_seconds)
            if bot: await bot.send_message(chat_id=message.chat.id, text=rule.reply_text or " ")
            await session.commit(); return
        user = await UserRepository(session).get(biz.user_id)
        if user and user.ai_enabled:
            try:
                ai = AIService(AIHistoryRepository(session), UserService(UserRepository(session)))
                res = await ai.chat(user=user, chat_id=chat.id, message=message.text)
                if bot: await bot.send_message(chat_id=message.chat.id, text=res["reply"])
                await MessageService(msgs).save(chat_id=chat.id, telegram_message_id=0,
                    direction=MessageDirection.OUTGOING, message_type=MessageType.TEXT,
                    text=res["reply"], ai_used=True)
            except Exception as e:
                logger.exception("AI failed: %s", e)
        await session.commit()

    async def on_edit(self, message, *, session, **_): await session.commit()

    async def on_delete(self, event, *, session, **_):
        bizs = BusinessRepository(session)
        biz = await bizs.get_by_connection_id(event.business_connection_id)
        if not biz: return
        chat_ids_subq = select(ChatModel.id).where(ChatModel.business_id == biz.id)
        for mid in event.message_ids:
            await session.execute(update(MessageModel)
                .where(MessageModel.chat_id.in_(chat_ids_subq), MessageModel.telegram_message_id == mid)
                .values(is_deleted=True))
        await session.commit()
