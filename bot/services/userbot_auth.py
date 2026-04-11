"""
Сервис авторизации Pyrogram через Bot API.
Шаги: номер телефона → код → (2FA пароль) → сессия сохранена.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

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

# Сколько живёт pending-авторизация
AUTH_TTL = timedelta(minutes=10)


@dataclass
class PendingAuth:
    client: Client
    phone: str
    phone_code_hash: str
    created_at: datetime


# Временное хранилище клиентов в процессе авторизации
_pending_auth: dict[int, PendingAuth] = {}


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


def _is_pending_alive(pending: PendingAuth) -> bool:
    return datetime.now(timezone.utc) - pending.created_at <= AUTH_TTL


async def send_code(user_id: int, phone: str) -> dict:
    """
    Отправляет код верификации на телефон.
    Возвращает {"ok": True} или {"ok": False, "error": "..."}
    """
    now = datetime.now(timezone.utc)

    # Если уже есть активная попытка на тот же номер — не шлём новый код,
    # потому что новый код инвалидирует старый.
    existing = _pending_auth.get(user_id)
    if existing and _is_pending_alive(existing) and existing.phone == phone:
        return {"ok": True, "already_sent": True}

    # Если была старая попытка — закрываем её
    if existing:
        try:
            await existing.client.disconnect()
        except Exception:
            pass
        _pending_auth.pop(user_id, None)

    client = Client(
        name=f"auth_{user_id}",
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
        in_memory=True,
    )

    try:
        await client.connect()
        sent = await client.send_code(phone)

        # Сохраняем запись в БД (не критично для самого шага кода,
        # но полезно для истории)
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
            record.auth_data = {
                "phone_code_hash": sent.phone_code_hash,
                "created_at": now.isoformat(),
            }
            await session.commit()

        # Главное: храним hash и client в памяти
        _pending_auth[user_id] = PendingAuth(
            client=client,
            phone=phone,
            phone_code_hash=sent.phone_code_hash,
            created_at=now,
        )

        return {"ok": True}

    except FloodWait as e:
        try:
            await client.disconnect()
        except Exception:
            pass
        return {"ok": False, "error": f"Слишком много попыток. Подожди {e.value} секунд."}

    except Exception as e:
        try:
            await client.disconnect()
        except Exception:
            pass
        logger.error(f"send_code error for {user_id}: {e}")
        return {"ok": False, "error": str(e)}


async def sign_in(user_id: int, code: str) -> dict:
    """
    Подтверждает код.
    Возвращает:
    {"ok": True} — авторизован
    {"ok": False, "need_password": True} — нужен 2FA пароль
    {"ok": False, "error": "..."} — ошибка
    """
    pending = _pending_auth.get(user_id)
    if not pending:
        return {"ok": False, "error": "Сессия истекла. Начни заново с /userbot"}

    if not _is_pending_alive(pending):
        try:
            await pending.client.disconnect()
        except Exception:
            pass
        _pending_auth.pop(user_id, None)
        return {"ok": False, "error": "Код истёк. Начни заново с /userbot"}

    client = pending.client
    phone = pending.phone
    phone_code_hash = pending.phone_code_hash

    try:
        user = await client.sign_in(
            phone_number=phone,
            phone_code_hash=phone_code_hash,
            phone_code=code,
        )

        # На всякий случай оставим обработку ToS
        if isinstance(user, TermsOfService):
            # В некоторых сценариях Pyrogram может вернуть TOS вместо User
            # Оставляем безопасную попытку продолжить.
            try:
                await client.accept_terms_of_service(user.id)
                user = await client.sign_in(
                    phone_number=phone,
                    phone_code_hash=phone_code_hash,
                    phone_code=code,
                )
            except Exception:
                pass

        return await _finalize_session(user_id, client)

    except SessionPasswordNeeded:
        return {"ok": False, "need_password": True}

    except PhoneCodeInvalid:
        return {"ok": False, "error": "Неверный код. Попробуй ещё раз."}

    except PhoneCodeExpired:
        try:
            await client.disconnect()
        except Exception:
            pass
        _pending_auth.pop(user_id, None)
        return {"ok": False, "error": "Код истёк. Начни заново с /userbot"}

    except Exception as e:
        logger.error(f"sign_in error for {user_id}: {e}")
        return {"ok": False, "error": str(e)}


async def sign_in_2fa(user_id: int, password: str) -> dict:
    """Подтверждает 2FA пароль."""
    pending = _pending_auth.get(user_id)
    if not pending:
        return {"ok": False, "error": "Сессия истекла. Начни заново с /userbot"}

    if not _is_pending_alive(pending):
        try:
            await pending.client.disconnect()
        except Exception:
            pass
        _pending_auth.pop(user_id, None)
        return {"ok": False, "error": "Код истёк. Начни заново с /userbot"}

    client = pending.client

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
    session_string = await client.export_session_string()

    try:
        await client.disconnect()
    except Exception:
        pass

    _pending_auth.pop(user_id, None)

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