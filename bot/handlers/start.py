from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.subscription import get_or_create_user, get_user
from bot.keyboards.main import main_menu_kb, plans_kb, back_main_kb, language_kb
from bot.i18n import t, get_lang, LANGUAGES

router = Router()


def _get_user_lang(user_db) -> str:
    if user_db and user_db.lang:
        return user_db.lang
    return "en"


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    user = await get_or_create_user(session, message.from_user)

    # Если язык ещё не выбран — автоопределяем по Telegram language_code
    if not user.lang or user.lang == "en":
        detected = get_lang(message.from_user.language_code)
        if detected != user.lang:
            user.lang = detected
            await session.commit()

    lang = _get_user_lang(user)
    await message.answer(
        t("welcome", lang),
        reply_markup=main_menu_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "back:main")
async def cb_back_main(call: CallbackQuery, session: AsyncSession):
    user = await get_user(session, call.from_user.id)
    lang = _get_user_lang(user)
    await call.message.edit_text(
        t("welcome", lang),
        reply_markup=main_menu_kb(lang),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "lang:menu")
async def cb_lang_menu(call: CallbackQuery, session: AsyncSession):
    user = await get_user(session, call.from_user.id)
    lang = _get_user_lang(user)
    await call.message.edit_text(
        t("choose_language", lang),
        reply_markup=language_kb(),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data.startswith("lang:set:"))
async def cb_lang_set(call: CallbackQuery, session: AsyncSession):
    new_lang = call.data.split(":")[2]
    if new_lang not in LANGUAGES:
        await call.answer("Unknown language", show_alert=True)
        return

    user = await get_user(session, call.from_user.id)
    if user:
        user.lang = new_lang
        await session.commit()

    await call.message.edit_text(
        t("language_set", new_lang),
        parse_mode="HTML",
    )
    await call.answer()

    # Возвращаем главное меню на новом языке
    await call.message.answer(
        t("welcome", new_lang),
        reply_markup=main_menu_kb(new_lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "help:connect")
async def cb_help_connect(call: CallbackQuery, session: AsyncSession):
    user = await get_user(session, call.from_user.id)
    lang = _get_user_lang(user)
    me = await call.bot.get_me()
    text = t("how_to_connect", lang, bot_username=me.username)
    await call.message.edit_text(
        text,
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "sub:status")
async def cb_status(call: CallbackQuery, session: AsyncSession):
    from datetime import datetime, timezone
    from sqlalchemy import select
    from db.models import Subscription

    user = await get_user(session, call.from_user.id)
    lang = _get_user_lang(user)
    now = datetime.now(timezone.utc)

    sub = None
    if user:
        result = await session.execute(
            select(Subscription)
            .where(
                Subscription.user_id == user.id,
                Subscription.is_active == True,
                Subscription.expires_at > now,
            )
            .order_by(Subscription.expires_at.desc())
            .limit(1)
        )
        sub = result.scalar_one_or_none()

    if sub:
        expires = sub.expires_at.strftime("%d.%m.%Y %H:%M")
        plan_names = {
            "trial":  {"ru": "Пробный", "en": "Trial", "pt": "Teste", "id": "Percobaan"},
            "week":   {"ru": "7 дней",  "en": "7 days", "pt": "7 dias", "id": "7 hari"},
            "month":  {"ru": "30 дней", "en": "30 days", "pt": "30 dias", "id": "30 hari"},
            "year":   {"ru": "1 год",   "en": "1 year", "pt": "1 ano", "id": "1 tahun"},
        }
        plan_label = plan_names.get(sub.plan.value, {}).get(lang, sub.plan.value)
        connected = t("connected_yes" if user.business_connection_id else "connected_no", lang)
        text = t("sub_active", lang, plan=plan_label, expires=expires, connected=connected)
    else:
        text = t("sub_inactive", lang)

    trial_ok = not user.trial_used if user else True
    await call.message.edit_text(
        text,
        reply_markup=plans_kb(lang, trial_ok),
        parse_mode="HTML",
    )
    await call.answer()
