from datetime import datetime, timezone, timedelta
import logging
import re

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
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


# Лимиты Telegram считаются по тексту после разбора разметки; берём с запасом
# на заголовок и подпись бота.
_TEXT_BUDGET = 3500
_CAPTION_BUDGET = 700
# Длинные цитаты сворачиваем — так делает и сам Telegram.
_EXPANDABLE_FROM = 300


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _who(lang: str, user_id: int | None, first_name: str | None, username: str | None) -> str:
    """Имя отправителя как в журнале действий Telegram: жирное, ссылкой на профиль."""
    name = f"<b>{_escape(first_name or t('unknown_sender', lang))}</b>"
    if user_id:
        name = f'<a href="tg://user?id={user_id}">{name}</a>'
    if username:
        name += f" (@{_escape(username)})"
    return name


def _quote(text: str, title: str | None = None) -> str:
    body = _escape(text)
    if title:
        body = f"<b>{title}</b>\n{body}"
    tag = "<blockquote expandable>" if len(text) > _EXPANDABLE_FROM else "<blockquote>"
    return f"{tag}{body}</blockquote>"


async def _format_notice(bot: Bot, header: str, quote: str | None = None) -> str:
    body = f"{header}\n{quote}" if quote else header
    return f"{body}\n\n{await _bot_promo(bot)}"


_USER_LINK = re.compile(r'<a href="tg://user\?id=\d+">(.*?)</a>', re.S)


async def _with_link_fallback(send, text: str) -> None:
    """Ссылка на профиль — косметика. Если Telegram отклонил разметку, шлём то же
    без ссылки, чтобы уведомление не потерялось."""
    try:
        await send(text)
    except TelegramBadRequest:
        plain = _USER_LINK.sub(r"\1", text)
        if plain == text:
            raise
        logger.warning("Notice rejected with a profile link, resending without it")
        await send(plain)


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


async def _format_deleted_from_cache(bot: Bot, snapshot: SavedMessage, lang: str, limit: int) -> str:
    who = _who(lang, snapshot.from_user_id, snapshot.from_first_name, snapshot.from_username)
    header = t("deleted_notice", lang, name=who)

    if snapshot.original_text:
        quote = _quote(_clip(snapshot.original_text, limit))
    elif snapshot.media_file_id:
        quote = None  # само медиа придёт следом, пояснять нечем
    else:
        quote = _quote(t("media_unknown", lang))

    return await _format_notice(bot, header, quote)


async def _format_edited(bot: Bot, lang: str, who: str, original: str) -> str:
    # Новый текст не дублируем: он уже виден в самом чате.
    header = t("edited_notice", lang, name=who)
    quote = _quote(_clip(original, _TEXT_BUDGET), t("original_message", lang))
    return await _format_notice(bot, header, quote)


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

            has_media = bool(snapshot.media_file_id)
            # У кружков и стикеров подписи не бывает: заголовок идёт отдельным
            # сообщением (как «плашка» в журнале Telegram), а следом само медиа.
            captionless = snapshot.media_type in ("video_note", "sticker")
            limit = _CAPTION_BUDGET if has_media and not captionless else _TEXT_BUDGET
            text = await _format_deleted_from_cache(bot, snapshot, lang, limit)

            if has_media and not captionless:
                await _with_link_fallback(
                    lambda caption: _send_media(
                        bot, owner.id, snapshot.media_file_id, snapshot.media_type, caption
                    ),
                    text,
                )
            else:
                await _with_link_fallback(
                    lambda msg: bot.send_message(owner.id, msg, parse_mode="HTML"), text
                )
                if has_media:
                    await _send_media(bot, owner.id, snapshot.media_file_id, snapshot.media_type, "")

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

    if snapshot and old_text == new_text:
        return  # видимый текст не менялся (например, правка форматирования) — показывать нечего

    if not snapshot:
        original = t("not_saved", lang)
    elif old_text:
        original = old_text
    else:
        original = t("media_unknown", lang)  # раньше было медиа без подписи

    who = _who(
        lang,
        sender.id if sender else None,
        sender.first_name if sender else None,
        sender.username if sender else None,
    )
    notify = await _format_edited(bot, lang, who, original)

    await _with_link_fallback(
        lambda msg: bot.send_message(owner.id, msg, parse_mode="HTML"), notify
    )
