"""
Сервис защиты от перехвата («призрачный режим»).

Защищённого пользователя бот полностью игнорирует как отправителя:
не перехватывает его одноразовые медиа и не сохраняет удалённые/изменённые
сообщения. При попытке перехвата защищённый пользователь получает уведомление.

Список защищённых ID держим в памяти процесса: бот работает как единый процесс
(и polling, и вебхуки CryptoBot/Stars обрабатываются в нём же), поэтому кэш в
Redis не нужен и не создаёт риска ложного «не защищён» при холодном кэше.
"""
import logging
from datetime import datetime, timezone, timedelta
from html import escape

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.i18n import t
from db.base import AsyncSessionLocal
from db.models import ProtectedUser, InterceptionAttempt, User, SavedMessage

logger = logging.getLogger(__name__)

_protected_ids: set[int] = set()
_last_notified: dict[tuple[int, int], datetime] = {}
NOTIFY_COOLDOWN = timedelta(hours=24)


async def load_protected_ids() -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ProtectedUser.user_id))
        ids = set(result.scalars().all())
    _protected_ids.clear()
    _protected_ids.update(ids)
    logger.info(f"Loaded {len(_protected_ids)} protected users")


def is_protected(user_id: int | None) -> bool:
    return bool(user_id) and user_id in _protected_ids


def mark_protected(user_id: int) -> None:
    _protected_ids.add(user_id)


async def grant_protection(
    session: AsyncSession,
    user_id: int,
    payment_id: int | None = None,
) -> bool:
    """Выдаёт защиту пользователю (оплата или подарок от админа).

    Возвращает False, если пользователь уже был защищён (идемпотентно).
    Ретроактивно удаляет уже закэшированные сообщения этого отправителя.
    """
    existing = await session.get(ProtectedUser, user_id)
    if existing:
        return False

    session.add(ProtectedUser(user_id=user_id, payment_id=payment_id))
    await session.execute(
        delete(SavedMessage).where(SavedMessage.from_user_id == user_id)
    )
    await session.commit()

    mark_protected(user_id)
    return True


async def record_attempt(bot, protected_id: int, from_id: int | None) -> None:
    """Фиксирует заблокированную попытку перехвата и уведомляет защищённого.

    `from_id` — тот, кто пытался перехватить (владелец userbot-сессии / бизнес-бота).
    Уведомление отправляется не чаще одного раза в сутки на пару отправителей,
    чтобы поток медиа от одного человека не превращался в спам.
    """
    async with AsyncSessionLocal() as session:
        session.add(InterceptionAttempt(protected_id=protected_id, from_id=from_id))
        await session.commit()

    key = (protected_id, from_id or 0)
    now = datetime.now(timezone.utc)
    last = _last_notified.get(key)
    if last and now - last < NOTIFY_COOLDOWN:
        return
    _last_notified[key] = now

    async with AsyncSessionLocal() as session:
        owner = await session.get(User, protected_id)
        lang = owner.lang if owner and owner.lang else "en"
        spy = await session.get(User, from_id) if from_id else None

    if spy:
        name = spy.first_name or "?"
        if spy.username:
            name = f"{name} (@{spy.username})"
        name = escape(name)
    else:
        name = t("protection_someone", lang)

    try:
        await bot.send_message(
            protected_id,
            t("protection_attempt_notice", lang, name=name),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"Could not notify protected user {protected_id}: {e}")
