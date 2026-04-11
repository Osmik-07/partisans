"""
FSM-хендлер для авторизации userbot через бота.
Команда /userbot запускает процесс.
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.services import userbot_auth, userbot_manager

router = Router()


class AuthStates(StatesGroup):
    waiting_phone = State()
    waiting_code = State()
    waiting_password = State()


def _cancel_kb():
    b = InlineKeyboardBuilder()
    b.button(text="❌ Отмена", callback_data="userbot:cancel")
    return b.as_markup()


def _userbot_menu_kb(is_connected: bool):
    b = InlineKeyboardBuilder()
    if is_connected:
        b.button(text="🔴 Отключить userbot", callback_data="userbot:disconnect")
    else:
        b.button(text="🟢 Подключить userbot", callback_data="userbot:connect")
    b.button(text="« Назад", callback_data="back:main")
    b.adjust(1)
    return b.as_markup()


# ── /userbot — главный экран ──────────────────────────────────────────
@router.message(Command("userbot"))
async def cmd_userbot(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    client = userbot_manager.get_client(user_id)
    is_connected = client is not None

    if is_connected:
        text = (
            "👁 <b>Userbot активен</b>\n\n"
            "Твой аккаунт подключён. Одноразовые фото и видео "
            "будут перехватываться автоматически.\n\n"
            "Чтобы отключить — нажми кнопку ниже."
        )
    else:
        text = (
            "👁 <b>Userbot — перехват одноразовых медиа</b>\n\n"
            "Для перехвата одноразовых фото и видео нужно авторизовать "
            "твой аккаунт Telegram.\n\n"
            "⚠️ <b>Важно:</b> твоя сессия хранится только на сервере бота "
            "и используется исключительно для получения одноразовых сообщений. "
            "Бот не читает твою переписку и не передаёт данные третьим лицам.\n\n"
            "Нажми «Подключить» чтобы начать."
        )

    await message.answer(text, reply_markup=_userbot_menu_kb(is_connected), parse_mode="HTML")


# ── Начало авторизации ────────────────────────────────────────────────
@router.callback_query(F.data == "userbot:connect")
async def cb_connect(call: CallbackQuery, state: FSMContext):
    if not settings.telegram_api_id or not settings.telegram_api_hash:
        await call.message.edit_text(
            "⚠️ <b>API_ID и API_HASH не настроены.</b>\n\n"
            "Администратор должен добавить в .env:\n"
            "<code>TELEGRAM_API_ID=12345678</code>\n"
            "<code>TELEGRAM_API_HASH=abc123...</code>",
            parse_mode="HTML",
        )
        await call.answer()
        return

    await state.set_state(AuthStates.waiting_phone)
    await call.message.edit_text(
        "📱 <b>Введи номер телефона</b>\n\n"
        "Формат: <code>+79001234567</code>\n\n"
        "На него придёт код подтверждения от Telegram.",
        reply_markup=_cancel_kb(),
        parse_mode="HTML",
    )
    await call.answer()


# ── Получаем номер телефона ───────────────────────────────────────────
@router.message(AuthStates.waiting_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()

    # Базовая валидация
    if not phone.startswith("+") or len(phone) < 8:
        await message.answer(
            "❌ Неверный формат. Введи номер с кодом страны, например:\n"
            "<code>+79001234567</code>",
            parse_mode="HTML",
        )
        return

    await message.answer("⏳ Отправляю код...")

    result = await userbot_auth.send_code(message.from_user.id, phone)

    if result["ok"]:
        await state.set_state(AuthStates.waiting_code)
        await state.update_data(phone=phone)
        await message.answer(
            "✅ Код отправлен!\n\n"
            "📬 Введи код из Telegram (приложение или SMS).\n"
            "Если код пришёл как <code>12345</code>, введи <code>1 2 3 4 5</code> или <code>12345</code>.",
            reply_markup=_cancel_kb(),
            parse_mode="HTML",
        )
    else:
        await state.clear()
        await message.answer(
            f"❌ Ошибка: {result['error']}\n\nПопробуй снова: /userbot",
            parse_mode="HTML",
        )


# ── Получаем код ──────────────────────────────────────────────────────
@router.message(AuthStates.waiting_code)
async def process_code(message: Message, state: FSMContext):
    # Убираем пробелы (пользователи часто вводят "1 2 3 4 5")
    code = message.text.strip().replace(" ", "")

    await message.answer("⏳ Проверяю код...")

    result = await userbot_auth.sign_in(message.from_user.id, code)

    if result.get("ok"):
        await state.clear()
        await message.answer(
            "✅ <b>Userbot успешно подключён!</b>\n\n"
            "Теперь я буду перехватывать одноразовые фото и видео "
            "и присылать их тебе как файлы.\n\n"
            "Управление: /userbot",
            parse_mode="HTML",
        )
    elif result.get("need_password"):
        await state.set_state(AuthStates.waiting_password)
        await message.answer(
            "🔐 <b>Двухфакторная аутентификация</b>\n\n"
            "Введи пароль облачного шифрования Telegram (2FA).",
            reply_markup=_cancel_kb(),
            parse_mode="HTML",
        )
    else:
        error = result.get("error", "Неизвестная ошибка")
        if "expired" in error.lower() or "истёк" in error.lower():
            await state.clear()
        await message.answer(
            f"❌ {error}",
            reply_markup=_cancel_kb() if await state.get_state() else None,
            parse_mode="HTML",
        )


# ── Получаем 2FA пароль ───────────────────────────────────────────────
@router.message(AuthStates.waiting_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()

    # Сразу удаляем сообщение с паролем из чата
    try:
        await message.delete()
    except Exception:
        pass

    await message.answer("⏳ Проверяю пароль...")

    result = await userbot_auth.sign_in_2fa(message.from_user.id, password)

    if result.get("ok"):
        await state.clear()
        await message.answer(
            "✅ <b>Userbot успешно подключён!</b>\n\n"
            "Одноразовые фото и видео буду присылать как файлы.\n\n"
            "Управление: /userbot",
            parse_mode="HTML",
        )
    else:
        await message.answer(
            f"❌ {result.get('error', 'Ошибка')}",
            reply_markup=_cancel_kb(),
            parse_mode="HTML",
        )


# ── Отмена ────────────────────────────────────────────────────────────
@router.callback_query(F.data == "userbot:cancel")
async def cb_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    # Чистим pending клиент если есть
    from bot.services.userbot_auth import _pending_clients
    client = _pending_clients.pop(call.from_user.id, None)
    if client:
        try:
            await client.disconnect()
        except Exception:
            pass

    await call.message.edit_text(
        "❌ Авторизация отменена.\n\nВернуться: /userbot",
        parse_mode="HTML",
    )
    await call.answer()


# ── Отключение ────────────────────────────────────────────────────────
@router.callback_query(F.data == "userbot:disconnect")
async def cb_disconnect(call: CallbackQuery, state: FSMContext):
    await state.clear()
    ok = await userbot_auth.disconnect_session(call.from_user.id)

    if ok:
        await call.message.edit_text(
            "🔴 <b>Userbot отключён.</b>\n\n"
            "Перехват одноразовых медиа остановлен.\n\n"
            "Подключить снова: /userbot",
            parse_mode="HTML",
        )
    else:
        await call.message.edit_text(
            "⚠️ Сессия не найдена или уже отключена.\n\nУправление: /userbot",
            parse_mode="HTML",
        )
    await call.answer()
