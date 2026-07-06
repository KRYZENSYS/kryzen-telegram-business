from __future__ import annotations
import logging
from aiogram import Router
from aiogram.types import BusinessConnection, BusinessMessagesDeleted, Message
from app.business.dispatcher import BusinessEventDispatcher

logger = logging.getLogger(__name__)
router = Router(name="business")
dispatcher = BusinessEventDispatcher()

@router.business_connection()
async def on_business_connection(event: BusinessConnection, **kwargs) -> None:
    logger.info("Business connection update: id=%s user=%s", event.id, event.user_chat_id)
    await dispatcher.on_connection(event, **kwargs)

@router.business_message()
async def on_business_message(message: Message, **kwargs) -> None:
    if not message.business_connection_id: return
    await dispatcher.on_message(message, **kwargs)

@router.edited_business_message()
async def on_edited_business_message(message: Message, **kwargs) -> None:
    if not message.business_connection_id: return
    await dispatcher.on_edit(message, **kwargs)

@router.deleted_business_messages()
async def on_deleted_business_messages(event: BusinessMessagesDeleted, **kwargs) -> None:
    await dispatcher.on_delete(event, **kwargs)
