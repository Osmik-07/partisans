"""
Планировщик задач.
"""
import asyncio
import logging
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, update, delete
from aiogram import Bot

from db.base import AsyncSessionLocal
from db.models import Subscription, User, SavedMessage

logger = logging.getLogger(__name__)


async def deactivate_expired_subscriptions():
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            update(Subscription)
            .where(
                Subscription.is_active == True,
                Subscription.expires_at <= now,
            )
            .values(is_active=False)
            .returning(Subscription.user_id, Subscription.plan)
        )
        expired = result.all()
        await session.commit()

    if expired:
        logger.info(f"Deactivated {len(expired)} expired subscriptions")

    return expired


async def delete_expired_saved_messages():
    """Удаляет SavedMessage у которых истёк срок хранения (3 дня)."""
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            delete(SavedMessage).where(
                SavedMessage.expires_at.isnot(None),
                SavedMessage.expires_at <= now,
            )
        )
        await session.commit()
        if result.rowcount:
            logger.info(f"Deleted {result.rowcount} expired saved messages")


async def send_expiry_reminders(bot: Bot):
    now = datetime.now(timezone.utc)
    remind_window_start = now + timedelta(hours=23)
    remind_window_end = now + timedelta(hours=25)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Subscription.id, Subscription.user_id, Subscription.plan, Subscription.expires_at)
            .where(
                Subscription.is_active == True,
                Subscription.expires_at >= remind_window_start,
                Subscription.expires_at <= remind_window_end,
                Subscription.reminded_24h_at.is_(None),
            )
        )
        rows = result.all()

    reminded_ids: list[int] = []
    for sub_id, user_id, plan, expires_at in rows:
        expires_str = expires_at.strftime("%d.%m.%Y %H:%M UTC")
        try:
            await bot.send_message(
                user_id,
                f"<b>Подписка истекает через 24 часа</b>\n\n"
                f"Срок действия: до <b>{expires_str}</b>\n\n"
                "Продли сейчас, чтобы не потерять доступ.",
                reply_markup=_renew_kb(),
                parse_mode="HTML",
            )
            reminded_ids.append(sub_id)
        except Exception as e:
            logger.warning(f"Could not remind user {user_id}: {e}")

    if reminded_ids:
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(Subscription)
                .where(Subscription.id.in_(reminded_ids))
                .values(reminded_24h_at=now)
            )
            await session.commit()


async def notify_expired_users(bot: Bot, expired: list):
    for user_id, plan in expired:
        try:
            await bot.send_message(
                user_id,
                "<b>Ваша подписка истекла</b>\n\n"
                "Для продолжения отслеживания сообщений продлите подписку.",
                reply_markup=_renew_kb(),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.warning(f"Could not notify expired user {user_id}: {e}")


def _renew_kb():
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    b = InlineKeyboardBuilder()
    b.button(text="Продлить подписку", callback_data="sub:plans")
    return b.as_markup()


async def scheduler_loop(bot: Bot):
    logger.info("Scheduler started")
    reminder_tick = 0

    while True:
        try:
            expired = await deactivate_expired_subscriptions()
            if expired:
                await notify_expired_users(bot, expired)

            await delete_expired_saved_messages()

            reminder_tick += 1
            if reminder_tick >= 6:
                await send_expiry_reminders(bot)
                reminder_tick = 0

        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)

        await asyncio.sleep(600)


def start_scheduler(bot: Bot):
    asyncio.create_task(scheduler_loop(bot))
