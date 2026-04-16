"""
Менеджер Telethon клиентов.
"""
import io
import logging
from typing import Optional

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

from bot.config import settings
from db.base import AsyncSessionLocal

logger = logging.getLogger(__name__)

_clients: dict[int, TelegramClient] = {}
_bot = None


def set_bot(bot):
    global _bot
    _bot = bot


def get_client(user_id: int) -> Optional[TelegramClient]:
    return _clients.get(user_id)


async def create_client_from_session(user_id: int, session_string: str) -> TelegramClient:
    client = TelegramClient(
        StringSession(session_string),
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
    )
    await client.connect()
    _register_handlers(client, user_id)
    _clients[user_id] = client
    logger.info(f"Userbot started for user {user_id}")
    return client


async def stop_client(user_id: int):
    client = _clients.pop(user_id, None)
    if client:
        try:
            await client.disconnect()
        except Exception:
            pass
        logger.info(f"Userbot stopped for user {user_id}")


async def load_all_sessions():
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        from db.models import UserbotSession
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


def _register_handlers(client: TelegramClient, owner_id: int):

    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def on_new_message(event):
        msg = event.message
        media = msg.media

        ttl = getattr(media, "ttl_seconds", None)
        logger.info(f"[userbot:{owner_id}] MSG id={msg.id} "
                    f"media={type(media).__name__} ttl={ttl}")

        if not ttl:
            return

        logger.info(f"[userbot:{owner_id}] Vanishing media! TTL={ttl}")
        await _handle_vanishing_media(owner_id, event)


async def _handle_vanishing_media(owner_id: int, event):
    if not _bot:
        return

    msg = event.message
    sender = await event.get_sender()
    sender_name = getattr(sender, "first_name", "Неизвестный") or "Неизвестный"
    username = getattr(sender, "username", None)
    if username:
        sender_name += f" (@{username})"

    caption = f"📸 <b>Одноразовое медиа</b> от <b>{sender_name}</b>"

    try:
        client = get_client(owner_id)
        if not client:
            return

        file_bytes = io.BytesIO()
        await client.download_media(msg, file=file_bytes)
        file_bytes.seek(0)

        media = msg.media
        if isinstance(media, MessageMediaPhoto):
            file_bytes.name = "photo.jpg"
        elif isinstance(media, MessageMediaDocument):
            mime = getattr(media.document, "mime_type", "")
            file_bytes.name = "video.mp4" if "video" in mime else "file"
        else:
            file_bytes.name = "photo.jpg"

        await _bot.send_document(
            owner_id,
            document=file_bytes,
            caption=caption,
            parse_mode="HTML",
        )

        logger.info(f"[userbot:{owner_id}] Vanishing media sent successfully")

        async with AsyncSessionLocal() as db:
            from db.models import SavedMessage, MessageType
            saved = SavedMessage(
                owner_id=owner_id,
                message_type=MessageType.VANISHING_PHOTO,
                from_user_id=getattr(sender, "id", None),
                from_username=getattr(sender, "username", None),
                from_first_name=getattr(sender, "first_name", None),
                chat_id=msg.chat_id,
                message_id=msg.id,
            )
            db.add(saved)
            await db.commit()

    except Exception as e:
        logger.error(f"[userbot:{owner_id}] Failed to handle vanishing media: {e}")