from pathlib import Path

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, BotCommand
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.services.subscription import get_or_create_user, get_user, get_referral_summary
from bot.keyboards.main import main_menu_kb, payment_method_kb, back_main_kb, language_kb, referral_kb
from bot.i18n import t, get_lang, LANGUAGES

router = Router()
START_VIDEO_PATH = Path(__file__).resolve().parents[2] / "media" / "start.mp4"
CONNECT_VIDEO_PATH = Path(__file__).resolve().parents[2] / "media" / "connect.mp4"
REFERRAL_GUIDE_PATHS = [
    Path(__file__).resolve().parents[2] / "media" / "referral-stars.png",
    Path(__file__).resolve().parents[2] / "media" / "referral-stars.jpg",
    Path(__file__).resolve().parents[2] / "media" / "referral-stars.jpeg",
]


def _get_user_lang(user_db) -> str:
    if user_db and user_db.lang:
        return user_db.lang
    return "en"


async def set_bot_commands(bot) -> None:
    command_locales = {
        "ru": [
            BotCommand(command="start", description=t("command_start_desc", "ru")),
            BotCommand(command="premium", description=t("command_premium_desc", "ru")),
        ],
        "en": [
            BotCommand(command="start", description=t("command_start_desc", "en")),
            BotCommand(command="premium", description=t("command_premium_desc", "en")),
        ],
        "pt": [
            BotCommand(command="start", description=t("command_start_desc", "pt")),
            BotCommand(command="premium", description=t("command_premium_desc", "pt")),
        ],
        "id": [
            BotCommand(command="start", description=t("command_start_desc", "id")),
            BotCommand(command="premium", description=t("command_premium_desc", "id")),
        ],
    }

    for lang_code, commands in command_locales.items():
        await bot.set_my_commands(commands, language_code=lang_code)

    await bot.set_my_commands(command_locales["en"])


async def send_welcome(message: Message, lang: str) -> None:
    if START_VIDEO_PATH.exists():
        await message.answer_video(FSInputFile(START_VIDEO_PATH))

    await message.answer(
        t("welcome", lang),
        reply_markup=main_menu_kb(lang),
        parse_mode="HTML",
    )


def _extract_start_payload(message: Message) -> str:
    parts = (message.text or "").split(maxsplit=1)
    return parts[1].strip() if len(parts) > 1 else ""


def _extract_referrer_id(payload: str) -> int | None:
    if not payload.startswith("ref_"):
        return None
    try:
        return int(payload.split("_", 1)[1])
    except ValueError:
        return None


async def _send_optional_video(message: Message, path: Path) -> None:
    if path.exists():
        await message.answer_video(FSInputFile(path))


async def _send_optional_photo(message: Message, paths: list[Path]) -> None:
    for path in paths:
        if path.exists():
            await message.answer_photo(FSInputFile(path))
            return


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    payload = _extract_start_payload(message)
    referrer_id = _extract_referrer_id(payload)
    user = await get_or_create_user(session, message.from_user, referred_by_id=referrer_id)

    # Если язык ещё не выбран — автоопределяем по Telegram language_code
    if not user.lang or user.lang == "en":
        detected = get_lang(message.from_user.language_code)
        if detected != user.lang:
            user.lang = detected
            await session.commit()

    lang = _get_user_lang(user)
    await send_welcome(message, lang)


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
    await _send_optional_video(call.message, CONNECT_VIDEO_PATH)
    await call.message.answer(
        text,
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "ref:menu")
async def cb_referral_menu(call: CallbackQuery, session: AsyncSession):
    user = await get_user(session, call.from_user.id)
    lang = _get_user_lang(user)
    summary = await get_referral_summary(session, call.from_user.id)
    me = await call.bot.get_me()
    referral_url = f"https://t.me/{me.username}?start=ref_{call.from_user.id}"
    share_text = t("referral_share_text", lang)
    await _send_optional_photo(call.message, REFERRAL_GUIDE_PATHS)
    text = t(
        "referral_program",
        lang,
        bonus_days=settings.referral_bonus_days,
        invites_count=summary["invites_count"],
        total_bonus_days=summary["total_bonus_days"],
        stars_percent=settings.referral_stars_percent,
        referral_url=referral_url,
    )
    await call.message.edit_text(
        text,
        reply_markup=referral_kb(lang, referral_url, share_text),
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
            "bonus":  {"ru": "Бонус",   "en": "Bonus", "pt": "Bônus", "id": "Bonus"},
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
        reply_markup=payment_method_kb(lang, trial_available=trial_ok),
        parse_mode="HTML",
    )
    await call.answer()
