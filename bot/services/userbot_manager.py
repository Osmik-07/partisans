"""
Менеджер Pyrogram клиентов.
Каждый пользователь = отдельный Client, работающий в фоне.
"""
import asyncio
import logging
import io
from typing import Optional

from pyrogram import Client, filters
from pyrogram.types import Message as PyroMessage
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

from bot.config import settings
from db.base import AsyncSessionLocal
from db.models import UserbotSession, User

logger = logging.getLogger(__name__)

# Словарь активных клиентов: user_id -> Client
_clients: dict[int, Client] = {}

# Aiogram bot instance (устанавливается при старте)
_bot = None


def set_bot(bot):
    global _bot
    _bot = bot


def get_client(user_id: int) -> Optional[Client]:
    return _clients.get(user_id)


async def create_client_from_session(user_id: int, session_string: str) -> Client:
    """Создаёт и запускает Pyrogram клиент из строки сессии."""
    client = Client(
        name=f"user_{user_id}",
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
        session_string=session_string,
        in_memory=True,
        no_updates=False,
    )
    _register_handlers(client, user_id)
    await client.start()
    _clients[user_id] = client
    logger.info(f"Userbot started for user {user_id}")
    return client


async def stop_client(user_id: int):
    """Останавливает клиент пользователя."""
    client = _clients.pop(user_id, None)
    if client:
        try:
            await client.stop()
        except Exception:
            pass
        logger.info(f"Userbot stopped for user {user_id}")


async def load_all_sessions():
    """При старте бота загружает все активные сессии из БД."""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(UserbotSession).where(
                UserbotSession.is_active == True,
                UserbotSession.session_string.isnot(None),
            )
        )
        sessions = result.scalars().all()

    for s in sessions:
        try:
            await create_client_from_session(s.user_id, s.session_string)
        except Exception as e:
            logger.error(f"Failed to load session for user {s.user_id}: {e}")

    logger.info(f"Loaded {len(sessions)} userbot sessions")


def _register_handlers(client: Client, owner_id: int):
    """Регистрирует обработчики для конкретного клиента."""

    @client.on_message(filters.private)
    async def on_any_message(c: Client, message: PyroMessage):
        """Логируем всё для отладки, перехватываем одноразовые медиа."""
        logger.info(f"[userbot:{owner_id}] MSG raw: {message}")
        try:
            # Проверяем ttl на объекте медиа, а не на сообщении
            ttl = None
            if message.photo:
                ttl = getattr(message.photo, "ttl_seconds", None)
            elif message.video:
                ttl = getattr(message.video, "ttl_seconds", None)

            if not ttl:
                return

            logger.info(f"[userbot:{owner_id}] Vanishing media detected! TTL={ttl}")
            await _handle_vanishing_media(owner_id, message)

        except Exception as e:
            logger.error(f"[userbot:{owner_id}] on_any_message error: {e}")

async def _handle_vanishing_media(owner_id: int, message: PyroMessage):
    """Скачивает одноразовое медиа и пересылает владельцу через бота."""
    if not _bot:
        return

    sender = message.from_user
    sender_name = sender.first_name if sender else "Неизвестный"
    if sender and sender.username:
        sender_name += f" (@{sender.username})"

    caption = f"📸 <b>Одноразовое медиа</b> от <b>{sender_name}</b>"

    try:
        # Скачиваем файл в память
        client = get_client(owner_id)
        if not client:
            return

        file_bytes = await client.download_media(message, in_memory=True)
        file_bytes = io.BytesIO(file_bytes.getvalue() if hasattr(file_bytes, 'getvalue') else bytes(file_bytes))
        file_bytes.seek(0)

        # Определяем тип и имя файла
        if message.photo:
            file_bytes.name = "photo.jpg"
            await _bot.send_document(
                owner_id,
                document=file_bytes,
                caption=caption,
                parse_mode="HTML",
            )
        elif message.video:
            file_bytes.name = "video.mp4"
            await _bot.send_document(
                owner_id,
                document=file_bytes,
                caption=caption,
                parse_mode="HTML",
            )
        else:
            file_bytes.name = "file"
            await _bot.send_document(
                owner_id,
                document=file_bytes,
                caption=caption,
                parse_mode="HTML",
            )

        logger.info(f"[userbot:{owner_id}] Vanishing media sent successfully")

        # Сохраняем в БД
        async with AsyncSessionLocal() as db:
            from db.models import SavedMessage, MessageType
            saved = SavedMessage(
                owner_id=owner_id,
                message_type=MessageType.VANISHING_PHOTO,
                from_user_id=sender.id if sender else None,
                from_username=sender.username if sender else None,
                from_first_name=sender.first_name if sender else None,
                chat_id=message.chat.id if message.chat else None,
                message_id=message.id,
            )
            db.add(saved)
            await db.commit()

    except Exception as e:
        logger.error(f"[userbot:{owner_id}] Failed to handle vanishing media: {e}")
