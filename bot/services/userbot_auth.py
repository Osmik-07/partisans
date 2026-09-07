"""
Сервис авторизации Telethon через Mini App.
Шаги: номер телефона → код → (2FA пароль) → сессия сохранена.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    FloodWaitError,
)

from bot.config import settings
from bot.services.security import encrypt_session_string
from db.base import AsyncSessionLocal
from db.models import UserbotSession

logger = logging.getLogger(__name__)

AUTH_TTL = timedelta(minutes=10)


@dataclass
class PendingAuth:
    client: TelegramClient
    phone: str
    phone_code_hash: str
    created_at: datetime


_pending_auth: dict[int, PendingAuth] = {}
PHONE_RE = re.compile(r"^\+[1-9]\d{6,14}$")


def _is_pending_alive(pending: PendingAuth) -> bool:
    return datetime.now(timezone.utc) - pending.created_at <= AUTH_TTL


async def cleanup_expired_pending_auth() -> None:
    """Отключает и удаляет заброшенные попытки логина (пользователь запросил код и пропал).

    Без этого каждая незавершённая попытка навсегда держит открытым
    MTProto-соединение в памяти процесса.
    """
    expired = [uid for uid, pending in _pending_auth.items() if not _is_pending_alive(pending)]
    for uid in expired:
        pending = _pending_auth.pop(uid, None)
        if not pending:
            continue
        try:
            await pending.client.disconnect()
        except Exception:
            pass
        logger.info(f"Cleaned up expired pending auth for user {uid}")


def normalize_phone(phone: str) -> str | None:
    digits = re.sub(r"[^\d+]", "", phone.strip())
    if digits.startswith("00"):
        digits = f"+{digits[2:]}"
    if not digits.startswith("+"):
        digits = f"+{digits.lstrip('+')}"
    digits = "+" + re.sub(r"\D", "", digits)
    if not PHONE_RE.fullmatch(digits):
        return None
    return digits


async def send_code(user_id: int, phone: str, accepted_terms: bool = False) -> dict:
    if not accepted_terms:
        return {"ok": False, "error": "You must accept the Privacy Policy and Terms of Use"}

    normalized_phone = normalize_phone(phone)
    if not normalized_phone:
        return {"ok": False, "error": "Invalid phone number"}

    now = datetime.now(timezone.utc)

    existing = _pending_auth.get(user_id)
    if existing and _is_pending_alive(existing) and existing.phone == normalized_phone:
        return {"ok": True, "already_sent": True}

    if existing:
        try:
            await existing.client.disconnect()
        except Exception:
            pass
        _pending_auth.pop(user_id, None)

    client = TelegramClient(
        StringSession(),
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
    )

    try:
        await client.connect()
        result = await client.send_code_request(normalized_phone)

        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(UserbotSession).where(UserbotSession.user_id == user_id)
            )
            record = res.scalar_one_or_none()
            if not record:
                record = UserbotSession(user_id=user_id, phone=normalized_phone)
                session.add(record)
            else:
                record.phone = normalized_phone
            record.auth_data = {
                "phone_code_hash": result.phone_code_hash,
                "created_at": now.isoformat(),
            }
            # Отметку о согласии не перезаписываем повторно — фиксируем только первый раз.
            if not record.terms_accepted_at:
                record.terms_accepted_at = now
            await session.commit()

        _pending_auth[user_id] = PendingAuth(
            client=client,
            phone=normalized_phone,
            phone_code_hash=result.phone_code_hash,
            created_at=now,
        )
        return {"ok": True}

    except FloodWaitError as e:
        try:
            await client.disconnect()
        except Exception:
            pass
        return {"ok": False, "error": f"Слишком много попыток. Подожди {e.seconds} секунд."}

    except Exception as e:
        try:
            await client.disconnect()
        except Exception:
            pass
        logger.error(f"send_code error for {user_id}: {e}")
        return {"ok": False, "error": str(e)}


async def sign_in(user_id: int, code: str) -> dict:
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
        await client.sign_in(
            phone=pending.phone,
            code=code,
            phone_code_hash=pending.phone_code_hash,
        )
        return await _finalize_session(user_id, client)

    except SessionPasswordNeededError:
        return {"ok": False, "need_password": True}

    except PhoneCodeInvalidError:
        return {"ok": False, "error": "Неверный код. Попробуй ещё раз."}

    except PhoneCodeExpiredError:
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
        await client.sign_in(password=password)
        return await _finalize_session(user_id, client)

    except Exception as e:
        if "password" in str(e).lower() or "invalid" in str(e).lower():
            return {"ok": False, "error": "Неверный пароль. Попробуй ещё раз."}
        logger.error(f"2fa error for {user_id}: {e}")
        return {"ok": False, "error": str(e)}


async def _finalize_session(user_id: int, client: TelegramClient) -> dict:
    session_string = client.session.save()
    encrypted_session_string = encrypt_session_string(session_string)

    try:
        await client.disconnect()
    except Exception:
        pass

    _pending_auth.pop(user_id, None)

    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(UserbotSession).where(UserbotSession.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        if record:
            record.session_string = encrypted_session_string
            record.is_active = True
            record.auth_data = None
            record.last_active = datetime.now(timezone.utc)
        await session.commit()

    from bot.services.userbot_manager import create_client_from_session
    await create_client_from_session(user_id, encrypted_session_string)

    return {"ok": True}


async def disconnect_session(user_id: int) -> bool:
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
