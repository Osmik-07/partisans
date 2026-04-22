from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.config import settings
from bot.keyboards.main import userbot_kb, back_main_kb
from bot.i18n import t
from bot.services.userbot_manager import get_client
from bot.services.subscription import get_active_subscription
from db.models import UserbotSession

router = Router()


def _lang(user_db) -> str:
    return user_db.lang if user_db and user_db.lang else "en"


@router.callback_query(F.data == "userbot:menu")
async def cb_userbot_menu(call: CallbackQuery, session: AsyncSession):
    from bot.services.subscription import get_user
    user = await get_user(session, call.from_user.id)
    lang = _lang(user)
    active_sub = await get_active_subscription(session, call.from_user.id)
    if not active_sub:
        await call.message.edit_text(
            t("sub_inactive", lang),
            reply_markup=back_main_kb(lang),
            parse_mode="HTML",
        )
        await call.answer()
        return

    # Проверяем активна ли сессия
    result = await session.execute(
        select(UserbotSession)
        .where(UserbotSession.user_id == call.from_user.id,
               UserbotSession.is_active == True)
    )
    record = result.scalar_one_or_none()
    client = get_client(call.from_user.id)
    is_active = record is not None and client is not None

    miniapp_url = f"https://{settings.miniapp_domain}/auth"

    if is_active:
        text = t("userbot_active", lang)
    else:
        text = t("userbot_title", lang)

    await call.message.edit_text(
        text,
        reply_markup=userbot_kb(lang, is_active, miniapp_url),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "userbot:disconnect")
async def cb_userbot_disconnect(call: CallbackQuery, session: AsyncSession):
    from bot.services.subscription import get_user
    from bot.services.userbot_auth import disconnect_session

    user = await get_user(session, call.from_user.id)
    lang = _lang(user)

    await disconnect_session(call.from_user.id)

    await call.message.edit_text(
        "🔴 " + {
            "ru": "Перехват отключён.",
            "en": "Interception disabled.",
            "pt": "Interceptação desativada.",
            "id": "Intersepsi dinonaktifkan.",
        }.get(lang, "Interception disabled."),
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
    await call.answer()
