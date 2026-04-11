"""
Сервис авторизации Pyrogram через Bot API.
Шаги: номер телефона → код → (2FA пароль) → сессия сохранена.
"""
import logging
from pyrogram import Client
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    FloodWait,
    BadRequest,
)
from pyrogram.types import TermsOfService

from bot.config import settings
from db.base import AsyncSessionLocal
from db.models import UserbotSession

logger = logging.getLogger(__name__)


async def get_or_create_session_record(user_id: int) -> UserbotSession:
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(UserbotSession).where(UserbotSession.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        if not record:
            record = UserbotSession(user_id=user_id)
            session.add(record)
            await session.commit()
            await session.refresh(record)
        return record


async def send_code(user_id: int, phone: str) -> dict:
    """
    Отправляет код верификации на телефон.
    Возвращает {"ok": True} или {"ok": False, "error": "..."}
    """
    client = Client(
        name=f"auth_{user_id}",
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
        in_memory=True,
    )
    try:
        await client.connect()
        sent = await client.send_code(phone)

        # Сохраняем phone_code_hash для следующего шага
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(UserbotSession).where(UserbotSession.user_id == user_id)
            )
            record = result.scalar_one_or_none()
            if not record:
                record = UserbotSession(user_id=user_id, phone=phone)
                session.add(record)
            else:
                record.phone = phone
            record.auth_data = {"phone_code_hash": sent.phone_code_hash}
            await session.commit()

        # Сохраняем клиент временно в памяти для следующего шага
        _pending_clients[user_id] = client
        return {"ok": True}

    except FloodWait as e:
        await client.disconnect()
        return {"ok": False, "error": f"Слишком много попыток. Подожди {e.value} секунд."}
    except Exception as e:
        await client.disconnect()
        logger.error(f"send_code error for {user_id}: {e}")
        return {"ok": False, "error": str(e)}


async def sign_in(user_id: int, code: str) -> dict:
    """
    Подтверждает код. Возвращает:
    {"ok": True} — авторизован
    {"ok": False, "need_password": True} — нужен 2FA пароль
    {"ok": False, "error": "..."} — ошибка
    """
    client = _pending_clients.get(user_id)
    if not client:
        return {"ok": False, "error": "Сессия истекла. Начни заново с /userbot"}

    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(UserbotSession).where(UserbotSession.user_id == user_id)
        )
        record = result.scalar_one_or_none()

    if not record or not record.auth_data:
        return {"ok": False, "error": "Данные авторизации не найдены. Начни заново."}

    phone = record.phone
    phone_code_hash = record.auth_data["phone_code_hash"]

    try:
        user = await client.sign_in(phone, phone_code_hash, code)

        if isinstance(user, TermsOfService):
            await client.accept_terms_of_service(user.id)
            user = await client.sign_in(phone, phone_code_hash, code)

        return await _finalize_session(user_id, client)

    except SessionPasswordNeeded:
        return {"ok": False, "need_password": True}
    except PhoneCodeInvalid:
        return {"ok": False, "error": "Неверный код. Попробуй ещё раз."}
    except PhoneCodeExpired:
        _pending_clients.pop(user_id, None)
        return {"ok": False, "error": "Код истёк. Начни заново с /userbot"}
    except Exception as e:
        logger.error(f"sign_in error for {user_id}: {e}")
        return {"ok": False, "error": str(e)}


async def sign_in_2fa(user_id: int, password: str) -> dict:
    """Подтверждает 2FA пароль."""
    client = _pending_clients.get(user_id)
    if not client:
        return {"ok": False, "error": "Сессия истекла. Начни заново с /userbot"}

    try:
        await client.check_password(password)
        return await _finalize_session(user_id, client)
    except BadRequest:
        return {"ok": False, "error": "Неверный пароль. Попробуй ещё раз."}
    except Exception as e:
        logger.error(f"2fa error for {user_id}: {e}")
        return {"ok": False, "error": str(e)}


async def _finalize_session(user_id: int, client: Client) -> dict:
    """Сохраняет сессию в БД и запускает постоянный клиент."""
    from pyrogram.storage import MemoryStorage
    session_string = await client.export_session_string()
    await client.disconnect()
    _pending_clients.pop(user_id, None)

    # Сохраняем в БД
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(UserbotSession).where(UserbotSession.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        if record:
            record.session_string = session_string
            record.is_active = True
            record.auth_data = None
            from datetime import datetime, timezone
            record.last_active = datetime.now(timezone.utc)
        await session.commit()

    # Запускаем постоянный клиент
    from bot.services.userbot_manager import create_client_from_session
    await create_client_from_session(user_id, session_string)

    return {"ok": True}


async def disconnect_session(user_id: int) -> bool:
    """Деактивирует сессию пользователя."""
    from bot.services.userbot_manager import stop_client
    await stop_client(user_id)

    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(UserbotSession).where(UserbotSession.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        if record:
            record.is_active = False
            record.session_string = None
            await session.commit()
            return True
    return False


# Временное хранилище клиентов в процессе авторизации
_pending_clients: dict[int, Client] = {}
