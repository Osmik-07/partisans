from aiogram import Router, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from bot.config import settings
from bot.keyboards.main import admin_kb, back_main_kb
from bot.services.subscription import get_stats, grant_subscription, get_user_by_username
from db.models import User

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


async def _resolve_target_user(session: AsyncSession, target: str) -> User | None:
    """Находит пользователя по user_id или @username для админ-команд."""
    if target.startswith("@"):
        return await get_user_by_username(session, target)
    try:
        return await session.get(User, int(target))
    except ValueError:
        return None


# ── АДМИН ПАНЕЛЬ ─────────────────────────────────────────────

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("<b>Админ-панель</b>", reply_markup=admin_kb(), parse_mode="HTML")


# ── СТАТИСТИКА ───────────────────────────────────────────────

@router.callback_query(F.data == "admin:stats")
async def cb_admin_stats(call: CallbackQuery, session: AsyncSession):
    if not is_admin(call.from_user.id):
        await call.answer("Нет доступа", show_alert=True)
        return

    stats = await get_stats(session)
    text = (
        "<b>Статистика бота</b>\n\n"
        f"Всего пользователей: <b>{stats['total_users']}</b>\n"
        f"Активных подписок: <b>{stats['active_subs']}</b>\n"
        f"Доход (USD): <b>${stats['total_revenue_usd']}</b>\n"
    )

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    b = InlineKeyboardBuilder()
    b.button(text="Обновить", callback_data="admin:stats")
    b.button(text="« Назад", callback_data="admin:menu")
    b.adjust(1)

    await call.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "admin:menu")
async def cb_admin_menu(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer("Нет доступа", show_alert=True)
        return

    await call.message.edit_text(
        "<b>Админ-панель</b>",
        reply_markup=admin_kb(),
        parse_mode="HTML"
    )
    await call.answer()


# ── ПОЛЬЗОВАТЕЛИ ─────────────────────────────────────────────

@router.callback_query(F.data == "admin:users")
async def cb_admin_users(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    await call.message.edit_text(
        "<b>Управление пользователями</b>\n\n"
        "Команды:\n"
        "/ban <code>user_id</code>\n"
        "/unban <code>user_id</code>\n"
        "/userinfo <code>user_id</code>",
        reply_markup=back_main_kb(),
        parse_mode="HTML",
    )
    await call.answer()


@router.message(Command("ban"))
async def cmd_ban(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Использование: /ban <user_id>")
        return

    try:
        uid = int(parts[1])
    except ValueError:
        await message.answer("Неверный ID")
        return

    user = await session.get(User, uid)
    if not user:
        await message.answer("Пользователь не найден")
        return

    user.is_banned = True
    await session.commit()

    await message.answer(f"Пользователь {uid} заблокирован")


@router.message(Command("unban"))
async def cmd_unban(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Использование: /unban <user_id>")
        return

    try:
        uid = int(parts[1])
    except ValueError:
        await message.answer("Неверный ID")
        return

    user = await session.get(User, uid)
    if not user:
        await message.answer("Пользователь не найден")
        return

    user.is_banned = False
    await session.commit()

    await message.answer(f"Пользователь {uid} разблокирован")


@router.message(Command("userinfo"))
async def cmd_userinfo(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Использование: /userinfo <user_id>")
        return

    try:
        uid = int(parts[1])
    except ValueError:
        await message.answer("Неверный ID")
        return

    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    result = await session.execute(
        select(User)
        .options(selectinload(User.subscriptions))
        .where(User.id == uid)
    )
    user = result.scalar_one_or_none()

    if not user:
        await message.answer("Пользователь не найден")
        return

    sub = user.active_subscription
    sub_text = "нет"
    if sub:
        expires = sub.expires_at.strftime("%d.%m.%Y")
        sub_text = f"{sub.plan.value} до {expires}"

    text = (
        f"<b>Пользователь {uid}</b>\n"
        f"Имя: {user.first_name or '—'}\n"
        f"Username: @{user.username or '—'}\n"
        f"Бан: {'да' if user.is_banned else 'нет'}\n"
        f"Подписка: {sub_text}\n"
        f"Бизнес: {'подключён' if user.business_connection_id else 'нет'}\n"
        f"Зарегистрирован: {user.created_at.strftime('%d.%m.%Y')}"
    )

    await message.answer(text, parse_mode="HTML")


# ── РАССЫЛКА ────────────────────────────────────────────────

@router.callback_query(F.data == "admin:broadcast")
async def cb_broadcast_start(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    await call.message.edit_text(
        "<b>Рассылка</b>\n\n"
        "Отправь:\n<code>/broadcast текст</code>",
        reply_markup=back_main_kb(),
        parse_mode="HTML",
    )
    await call.answer()


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    text = message.text[len("/broadcast "):].strip()
    if not text:
        await message.answer("Использование: /broadcast <текст>")
        return

    from sqlalchemy import select
    result = await session.execute(select(User.id).where(User.is_banned == False))
    user_ids = [row[0] for row in result.all()]

    sent, failed = 0, 0

    for uid in user_ids:
        try:
            await message.bot.send_message(uid, text, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.05)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await message.bot.send_message(uid, text, parse_mode="HTML")
                sent += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1

    await message.answer(
        f"Рассылка завершена\n"
        f"Отправлено: {sent}\n"
        f"Ошибок: {failed}"
    )


# ── ПОДАРОК ПОДПИСКИ ─────────────────────────────────────

@router.callback_query(F.data == "admin:gift")
async def cb_admin_gift(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer("Нет доступа", show_alert=True)
        return

    await call.message.edit_text(
        "<b>Подарить подписку</b>\n\n"
        "Используй:\n"
        "<code>/gift 123456789 30</code>\n"
        "<code>/gift @username 30</code>",
        reply_markup=back_main_kb(),
        parse_mode="HTML",
    )
    await call.answer()


@router.message(Command("gift"))
async def cmd_gift(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Использование: /gift <user_id|@username> <days>")
        return

    target = parts[1]

    try:
        days = int(parts[2])
    except ValueError:
        await message.answer("Неверное число дней")
        return

    user = await _resolve_target_user(session, target)
    if not user:
        await message.answer("Пользователь не найден")
        return

    sub = await grant_subscription(session, user.id, days)

    await message.answer(
        f"Подписка выдана\n\n"
        f"Пользователь: <code>{user.id}</code>\n"
        f"Срок: {days} дней\n"
        f"До: {sub.expires_at.strftime('%d.%m.%Y %H:%M')}",
        parse_mode="HTML",
    )


# ── ПОДАРОК ЗАЩИТЫ ────────────────────────────────────────

@router.callback_query(F.data == "admin:gift_protection")
async def cb_admin_gift_protection(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer("Нет доступа", show_alert=True)
        return

    await call.message.edit_text(
        "<b>Подарить защиту</b>\n\n"
        "Разово и навсегда делает пользователя невидимым внутри бота "
        "(одноразовые медиа + удалённые/изменённые сообщения).\n\n"
        "Используй:\n"
        "<code>/protect 123456789</code>\n"
        "<code>/protect @username</code>",
        reply_markup=back_main_kb(),
        parse_mode="HTML",
    )
    await call.answer()


@router.message(Command("protect"))
async def cmd_protect(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    from bot.services.protection import grant_protection, is_protected

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Использование: /protect <user_id|@username>")
        return

    user = await _resolve_target_user(session, parts[1])
    if not user:
        await message.answer("Пользователь не найден")
        return

    if is_protected(user.id):
        await message.answer(f"Пользователь <code>{user.id}</code> уже под защитой", parse_mode="HTML")
        return

    await grant_protection(session, user.id)

    await message.answer(
        f"Защита выдана\n\n"
        f"Пользователь: <code>{user.id}</code>\n"
        f"Разово, без срока действия.",
        parse_mode="HTML",
    )
