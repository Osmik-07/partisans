from datetime import datetime, timezone, timedelta
import logging

from aiogram import Router, Bot
from aiogram.types import BusinessMessagesDeleted, Message, BusinessConnection
from sqlalchemy import select

from bot.i18n import t
from db.base import AsyncSessionLocal
from db.models import User, SavedMessage, MessageType

router = Router()
logger = logging.getLogger(__name__)
_bot_promo_cache: str | None = None


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


async def _bot_promo(bot: Bot) -> str:
    global _bot_promo_cache
    if not _bot_promo_cache:
        me = await bot.get_me()
        _bot_promo_cache = f"<code>@{me.username}</code>" if me.username else "<code>Partisans</code>"
    return _bot_promo_cache


async def _format_notice(bot: Bot, title: str, sender_name: str, body: list[str], lang: str) -> str:
    lines = [
        f"<b>{title}</b>",
        f"{t('sender_label', lang)}:",
        f"<blockquote>{_escape(sender_name)}</blockquote>",
    ]
    lines.extend(body)
    joined = "\n\n".join(lines)
    return f"{joined}\n\n{await _bot_promo(bot)}"


# Расширенная поддержка медиа
def _extract_media(message: Message):
    if message.photo:
        return message.photo[-1].file_id, "photo"
    if message.video:
        return message.video.file_id, "video"
    if message.animation:
        return message.animation.file_id, "animation"
    if message.audio:
        return message.audio.file_id, "audio"
    if message.voice:
        return message.voice.file_id, "voice"
    if message.video_note:
        return message.video_note.file_id, "video_note"
    if message.sticker:
        return message.sticker.file_id, "sticker"
    if message.document:
        return message.document.file_id, "document"
    return None, None


async def _format_deleted_from_cache(bot: Bot, snapshot: SavedMessage, lang: str) -> str:
    sender_name = snapshot.from_first_name or "Неизвестный"
    if snapshot.from_username:
        sender_name = f"{sender_name} (@{snapshot.from_username})"

    if snapshot.original_text:
        body = [f"<blockquote>{_escape(snapshot.original_text)}</blockquote>"]
    elif snapshot.media_type == "photo":
        body = [f"<blockquote>{t('media_photo', lang)}</blockquote>"]
    elif snapshot.media_type == "video":
        body = [f"<blockquote>{t('media_video', lang)}</blockquote>"]
    elif snapshot.media_type == "animation":
        body = [f"<blockquote>{t('media_animation', lang)}</blockquote>"]
    elif snapshot.media_type == "audio":
        body = [f"<blockquote>{t('media_audio', lang)}</blockquote>"]
    elif snapshot.media_type == "voice":
        body = [f"<blockquote>{t('media_voice', lang)}</blockquote>"]
    elif snapshot.media_type == "video_note":
        body = [f"<blockquote>{t('media_video_note', lang)}</blockquote>"]
    elif snapshot.media_type == "sticker":
        body = [f"<blockquote>{t('media_sticker', lang)}</blockquote>"]
    elif snapshot.media_type == "document":
        body = [f"<blockquote>{t('media_document', lang)}</blockquote>"]
    else:
        body = [f"<blockquote>{t('media_unknown', lang)}</blockquote>"]

    return await _format_notice(bot, t("deleted_title", lang), sender_name, body, lang)


async def _get_business_owner(business_connection_id: str) -> User | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User)
            .where(
                User.business_connection_id == business_connection_id,
                User.is_banned == False,
            )
            .order_by(User.business_connected_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


async def _get_snapshot(session, owner_id: int, message_id: int) -> SavedMessage | None:
    result = await session.execute(
        select(SavedMessage)
        .where(
            SavedMessage.owner_id == owner_id,
            SavedMessage.message_id == message_id,
        )
        .order_by(SavedMessage.event_at.asc())
    )
    rows = result.scalars().all()
    if not rows:
        return None

    for row in rows:
        if row.extra_data and row.extra_data.get("snapshot"):
            return row

    return rows[0]


async def _send_media(bot: Bot, chat_id: int, file_id: str, media_type: str, caption: str):
    if media_type == "photo":
        await bot.send_photo(chat_id, file_id, caption=caption, parse_mode="HTML")
    elif media_type == "video":
        await bot.send_video(chat_id, file_id, caption=caption, parse_mode="HTML")
    elif media_type == "animation":
        await bot.send_animation(chat_id, file_id, caption=caption, parse_mode="HTML")
    elif media_type == "audio":
        await bot.send_audio(chat_id, file_id, caption=caption, parse_mode="HTML")
    elif media_type == "voice":
        await bot.send_voice(chat_id, file_id, caption=caption, parse_mode="HTML")
    elif media_type == "video_note":
        await bot.send_video_note(chat_id, file_id)
    elif media_type == "sticker":
        await bot.send_sticker(chat_id, file_id)
    elif media_type == "document":
        await bot.send_document(chat_id, file_id, caption=caption, parse_mode="HTML")
    else:
        await bot.send_message(chat_id, caption, parse_mode="HTML")


# ── Подключение бизнеса ─────────────────────────
@router.business_connection()
async def on_business_connection(bc: BusinessConnection):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, bc.user.id)
        if not user:
            return

        if bc.is_enabled:
            user.business_connection_id = bc.id
            user.business_connected_at = datetime.now(timezone.utc)
            await session.commit()
        else:
            user.business_connection_id = None
            await session.commit()


# ── КЕШ ─────────────────────────
@router.business_message()
async def on_business_message(message: Message):
    if not message.business_connection_id:
        return

    owner = await _get_business_owner(message.business_connection_id)
    if not owner:
        return

    sender = message.from_user

    from bot.services.protection import is_protected
    if sender and is_protected(sender.id):
        return  # отправитель под защитой — ничего не кэшируем

    text = message.text or message.caption or ""

    # DEBUG: входящие бизнес-сообщения
    logger.info(
        "MSG id=%s photo=%s video=%s animation=%s audio=%s doc=%s voice=%s video_note=%s spoiler=%s",
        message.message_id,
        bool(message.photo),
        bool(message.video),
        bool(message.animation),
        bool(message.audio),
        bool(message.document),
        bool(message.voice),
        bool(message.video_note),
        getattr(message, "has_media_spoiler", None),
    )

    media_file_id, media_type = _extract_media(message)

    async with AsyncSessionLocal() as session:
        snapshot = SavedMessage(
            owner_id=owner.id,
            message_type=MessageType.DELETED,
            from_user_id=sender.id if sender else None,
            from_username=sender.username if sender else None,
            from_first_name=sender.first_name if sender else None,
            chat_id=message.chat.id if message.chat else None,
            message_id=message.message_id,
            business_connection_id=message.business_connection_id,
            original_text=text,
            media_file_id=media_file_id,
            media_type=media_type,
            extra_data={"snapshot": True},
            expires_at=datetime.now(timezone.utc) + timedelta(days=3),
        )
        session.add(snapshot)
        await session.commit()


# ── Удалённые ─────────────────────────
@router.deleted_business_messages()
async def on_deleted_messages(event: BusinessMessagesDeleted, bot: Bot):
    owner = await _get_business_owner(event.business_connection_id)
    if not owner:
        return
    lang = owner.lang if owner.lang else "en"

    from bot.services.protection import is_protected

    async with AsyncSessionLocal() as session:
        for message_id in event.message_ids:
            snapshot = await _get_snapshot(session, owner.id, message_id)
            if not snapshot:
                continue

            if is_protected(snapshot.from_user_id):
                continue  # отправитель под защитой — не сообщаем об удалении

            text = await _format_deleted_from_cache(bot, snapshot, lang)

            if snapshot.media_file_id:
                await _send_media(
                    bot,
                    owner.id,
                    snapshot.media_file_id,
                    snapshot.media_type,
                    text,
                )
            else:
                await bot.send_message(owner.id, text, parse_mode="HTML")

        await session.commit()


# ── Редактирование ─────────────────────────
@router.edited_business_message()
async def on_edited_message(message: Message, bot: Bot):
    owner = await _get_business_owner(message.business_connection_id)
    if not owner:
        return
    lang = owner.lang if owner.lang else "en"

    sender = message.from_user

    from bot.services.protection import is_protected
    if sender and is_protected(sender.id):
        return  # отправитель под защитой — правки не отслеживаем

    new_text = message.text or message.caption or ""
    sender_name = sender.first_name if sender and sender.first_name else "Unknown"
    if sender and sender.username:
        sender_name = f"{sender_name} (@{sender.username})"

    async with AsyncSessionLocal() as session:
        snapshot = await _get_snapshot(session, owner.id, message.message_id)
        old_text = snapshot.original_text if snapshot else None
        if snapshot:
            # Обновляем кэш, чтобы следующая правка или удаление
            # сравнивались с актуальным текстом, а не с самой первой версией.
            snapshot.original_text = new_text
            media_file_id, media_type = _extract_media(message)
            if media_file_id:
                snapshot.media_file_id = media_file_id
                snapshot.media_type = media_type
            await session.commit()

    notify = await _format_notice(
        bot,
        t("edited_title", lang),
        sender_name,
        [
            f"{t('was', lang)}\n<blockquote>{_escape(old_text or t('not_saved', lang))}</blockquote>",
            f"{t('became', lang)}\n<blockquote>{_escape(new_text)}</blockquote>",
        ],
        lang,
    )

    await bot.send_message(owner.id, notify, parse_mode="HTML")
