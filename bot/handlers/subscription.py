from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.i18n import t
from bot.keyboards.main import (
    plans_kb,
    pay_crypto_kb,
    back_main_kb,
    payment_method_kb,
    protection_kb,
    protection_method_kb,
    support_kb,
    method_label,
    plan_price,
)
from bot.services import subscription as sub_svc
from bot.services import cryptobot as crypto_svc
from db.models import SubscriptionPlan, PaymentMethod, PaymentStatus

router = Router()

PLAN_MAP = {
    "trial": SubscriptionPlan.TRIAL,
    "week": SubscriptionPlan.WEEK,
    "month": SubscriptionPlan.MONTH,
    "year": SubscriptionPlan.YEAR,
}

PLAN_LABELS = {
    "trial": "Пробный период",
    "week": "7 дней",
    "month": "30 дней",
    "year": "1 год",
}


def _lang(user) -> str:
    return user.lang if user and user.lang else "en"


async def _send_plans_message(message: Message, session: AsyncSession):
    user = await sub_svc.get_user(session, message.from_user.id)
    trial_ok = not user.trial_used if user else True
    lang = _lang(user)
    await message.answer(
        t("method_title", lang),
        reply_markup=payment_method_kb(lang, trial_available=trial_ok),
        parse_mode="HTML",
    )


@router.message(Command("premium"))
async def cmd_premium(message: Message, session: AsyncSession):
    await _send_plans_message(message, session)


# ── Шаг 1: способ оплаты ────────────────────────────────────────────
@router.callback_query(F.data == "sub:plans")
async def cb_plans(call: CallbackQuery, session: AsyncSession):
    user = await sub_svc.get_user(session, call.from_user.id)
    trial_ok = not user.trial_used if user else True
    lang = _lang(user)
    await call.message.edit_text(
        t("method_title", lang),
        reply_markup=payment_method_kb(lang, trial_available=trial_ok),
        parse_mode="HTML",
    )
    await call.answer()


# ── Шаг 2: тариф в валюте выбранного способа ────────────────────────
@router.callback_query(F.data.regexp(r"^sub:m:(sbp|crypto|stars)$"))
async def cb_method(call: CallbackQuery, session: AsyncSession):
    method = call.data.split(":")[2]
    user = await sub_svc.get_user(session, call.from_user.id)
    lang = _lang(user)
    await call.message.edit_text(
        t("plans_title_method", lang, method=method_label(method, lang)),
        reply_markup=plans_kb(lang, method=method),
        parse_mode="HTML",
    )
    await call.answer()


# ── Поддержка и документы ───────────────────────────────────────────
@router.callback_query(F.data == "help:support")
async def cb_support(call: CallbackQuery, session: AsyncSession):
    user = await sub_svc.get_user(session, call.from_user.id)
    lang = _lang(user)
    await call.message.edit_text(
        t("support_title", lang, contact=settings.support_contact),
        reply_markup=support_kb(lang),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    await call.answer()


# ── Пробный период ──────────────────────────────────────────────────
@router.callback_query(F.data == "buy:trial")
async def cb_trial(call: CallbackQuery, session: AsyncSession):
    user = await sub_svc.get_or_create_user(session, call.from_user)
    lang = _lang(user)
    if user and user.trial_used:
        await call.answer(t("trial_already_used", lang), show_alert=True)
        return

    sub = await sub_svc.activate_trial_subscription(session, call.from_user.id)
    if not sub:
        await call.answer(t("trial_already_used", lang), show_alert=True)
        return

    await call.message.edit_text(
        t("trial_activated", lang, days=settings.price_trial_days),
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
    await call.answer()


# ── СБП ─────────────────────────────────────────────────────────────
@router.callback_query(F.data.regexp(r"^buy:sbp:(week|month|year)$"))
async def cb_pay_sbp(call: CallbackQuery, session: AsyncSession):
    """Заглушка до подключения эквайринга: платёж не создаётся.

    Когда PlateGo выдаст доступ, здесь появится создание счёта СБП; тариф и
    цена в рублях уже приходят в callback_data и берутся из настроек.
    """
    user = await sub_svc.get_user(session, call.from_user.id)
    lang = _lang(user)
    await call.message.edit_text(
        t("sbp_soon", lang),
        reply_markup=payment_method_kb(lang, trial_available=not (user and user.trial_used)),
        parse_mode="HTML",
    )
    await call.answer()


# ── Оплата крипто ───────────────────────────────────────────────────
# Формат callback_data — buy:crypto:<план>; старый pay:crypto:<план> оставлен,
# чтобы кнопки в уже отправленных сообщениях продолжали работать.
@router.callback_query(F.data.regexp(r"^(buy|pay):crypto:(week|month|year)$"))
async def cb_pay_crypto(call: CallbackQuery, session: AsyncSession):
    plan_key = call.data.split(":")[2]
    plan = PLAN_MAP.get(plan_key)
    if not plan:
        await call.answer("Неверный тариф", show_alert=True)
        return

    amounts = {
        "week": settings.price_week_usd,
        "month": settings.price_month_usd,
        "year": settings.price_year_usd,
    }
    amount = amounts[plan_key]

    payment = await sub_svc.create_payment(
        session,
        user_id=call.from_user.id,
        plan=plan,
        method=PaymentMethod.CRYPTOBOT,
        amount_usd=amount,
    )

    try:
        me = await call.bot.get_me()
        invoice = await crypto_svc.create_invoice(
            plan=plan,
            amount=amount,
            payload=str(payment.id),
            bot_username=me.username,
        )
    except Exception as e:
        await call.answer(f"Ошибка создания инвойса: {e}", show_alert=True)
        return

    payment.external_id = invoice["invoice_id"]
    payment.invoice_url = invoice["pay_url"]
    await session.commit()

    await call.message.edit_text(
        f"<b>Оплата через CryptoBot</b>\n\n"
        f"Тариф: <b>{PLAN_LABELS[plan_key]}</b>\n"
        f"Сумма: <b>${amount}</b>\n\n"
        f"Нажми «Оплатить», затем вернись и нажми «Я оплатил».",
        reply_markup=pay_crypto_kb(invoice["pay_url"], payment.id),
        parse_mode="HTML",
    )
    await call.answer()


# ── Проверка оплаты крипто ──────────────────────────────────────────
@router.callback_query(F.data.startswith("pay:check:"))
async def cb_pay_check(call: CallbackQuery, session: AsyncSession):
    from sqlalchemy import select
    from db.models import Payment

    try:
        payment_id = int(call.data.split(":")[2])
    except (IndexError, ValueError):
        await call.answer("Некорректный платёж.", show_alert=True)
        return

    result = await session.execute(
        select(Payment)
        .where(Payment.id == payment_id, Payment.user_id == call.from_user.id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        await call.answer("Платёж не найден.", show_alert=True)
        return

    if payment.status == PaymentStatus.PAID:
        if payment.product == "protection":
            from bot.services.protection import mark_protected
            mark_protected(payment.user_id)
            user = await sub_svc.get_user(session, call.from_user.id)
            lang = _lang(user)
            await call.message.edit_text(
                t("protection_active", lang),
                reply_markup=back_main_kb(lang),
                parse_mode="HTML",
            )
            await call.answer()
            return
        sub, _ = await sub_svc.confirm_payment(session, payment.id)
        expires = sub.expires_at.strftime("%d.%m.%Y")
        await call.message.edit_text(
            f"<b>Оплата уже подтверждена.</b>\n\n"
            f"Подписка активна до <b>{expires}</b>.",
            reply_markup=back_main_kb(),
            parse_mode="HTML",
        )
        await call.answer("Оплата уже подтверждена.")
        return

    if not payment.external_id:
        await call.answer("Для этого платежа ещё нет инвойса.", show_alert=True)
        return

    # Проверяем через CryptoBot API
    import aiohttp
    try:
        async with aiohttp.ClientSession() as http:
            resp = await http.get(
                f"{crypto_svc.CRYPTOBOT_API}/getInvoices",
                headers={"Crypto-Pay-API-Token": settings.cryptobot_token},
                params={"invoice_ids": payment.external_id},
            )
            data = await resp.json()
    except Exception:
        await call.answer("Не удалось проверить оплату. Попробуй позже.", show_alert=True)
        return

    if data.get("ok"):
        items = data["result"].get("items", [])
        if items and items[0]["status"] == "paid":
            if payment.product == "protection":
                await sub_svc.confirm_protection_payment(session, payment.id)
                user = await sub_svc.get_user(session, call.from_user.id)
                lang = _lang(user)
                await call.message.edit_text(
                    t("protection_activated", lang),
                    reply_markup=back_main_kb(lang),
                    parse_mode="HTML",
                )
                await call.answer()
                return
            sub, _ = await sub_svc.confirm_payment(session, payment.id)
            expires = sub.expires_at.strftime("%d.%m.%Y")
            await call.message.edit_text(
                f"<b>Оплата подтверждена.</b>\n\n"
                f"Подписка активна до <b>{expires}</b>.\n\n"
                f"Подключи бота: Настройки → Автоматизация чатов → Чат-боты",
                reply_markup=back_main_kb(),
                parse_mode="HTML",
            )
            await call.answer("Оплата подтверждена.")
            return

    await call.answer("Платёж ещё не найден. Попробуй через минуту.", show_alert=True)


# ── Telegram Stars ──────────────────────────────────────────────────
@router.callback_query(F.data.regexp(r"^(buy|pay):stars:(week|month|year)$"))
async def cb_pay_stars(call: CallbackQuery, session: AsyncSession):
    plan_key = call.data.split(":")[2]
    plan = PLAN_MAP.get(plan_key)
    if not plan:
        await call.answer("Неверный тариф", show_alert=True)
        return

    stars_map = {
        "week": settings.price_week_stars,
        "month": settings.price_month_stars,
        "year": settings.price_year_stars,
    }
    stars = stars_map[plan_key]

    payment = await sub_svc.create_payment(
        session,
        user_id=call.from_user.id,
        plan=plan,
        method=PaymentMethod.STARS,
        amount_stars=stars,
    )

    await call.message.answer_invoice(
        title=f"Partisans — {PLAN_LABELS[plan_key]}",
        description="Доступ к перехвату одноразовых фото и видео",
        payload=str(payment.id),
        currency="XTR",
        prices=[LabeledPrice(label="Stars", amount=stars)],
    )
    await call.answer()


# ── Защита от перехвата (разовый продукт) ───────────────────────────
@router.callback_query(F.data == "protect:menu")
async def cb_protect_menu(call: CallbackQuery, session: AsyncSession):
    from bot.services.protection import is_protected
    user = await sub_svc.get_user(session, call.from_user.id)
    lang = _lang(user)
    if is_protected(call.from_user.id):
        await call.message.edit_text(
            t("protection_active", lang),
            reply_markup=back_main_kb(lang),
            parse_mode="HTML",
        )
    else:
        await call.message.edit_text(
            t("protection_title", lang, price=f"{settings.price_protection_usd:.0f}"),
            reply_markup=protection_kb(lang, already_protected=False),
            parse_mode="HTML",
        )
    await call.answer()


@router.callback_query(F.data == "protect:pay")
async def cb_protect_pay(call: CallbackQuery, session: AsyncSession):
    from bot.services.protection import is_protected
    user = await sub_svc.get_user(session, call.from_user.id)
    lang = _lang(user)
    if is_protected(call.from_user.id):
        await call.answer(t("protection_already", lang), show_alert=True)
        return
    await call.message.edit_text(
        t("protection_choose_method", lang),
        reply_markup=protection_method_kb(lang),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "protect:crypto")
async def cb_protect_crypto(call: CallbackQuery, session: AsyncSession):
    from bot.services.protection import is_protected
    user = await sub_svc.get_or_create_user(session, call.from_user)
    lang = _lang(user)
    if is_protected(call.from_user.id):
        await call.answer(t("protection_already", lang), show_alert=True)
        return

    amount = settings.price_protection_usd
    payment = await sub_svc.create_payment(
        session,
        user_id=call.from_user.id,
        plan=None,
        method=PaymentMethod.CRYPTOBOT,
        amount_usd=amount,
        product="protection",
    )

    try:
        me = await call.bot.get_me()
        invoice = await crypto_svc.create_invoice(
            plan=None,
            amount=amount,
            payload=str(payment.id),
            bot_username=me.username,
            description="Partisans — Protection",
        )
    except Exception as e:
        await call.answer(f"Ошибка создания инвойса: {e}", show_alert=True)
        return

    payment.external_id = invoice["invoice_id"]
    payment.invoice_url = invoice["pay_url"]
    await session.commit()

    await call.message.edit_text(
        t("protection_pay_crypto", lang, price=f"{amount:.0f}"),
        reply_markup=pay_crypto_kb(invoice["pay_url"], payment.id),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "protect:stars")
async def cb_protect_stars(call: CallbackQuery, session: AsyncSession):
    from bot.services.protection import is_protected
    user = await sub_svc.get_or_create_user(session, call.from_user)
    lang = _lang(user)
    if is_protected(call.from_user.id):
        await call.answer(t("protection_already", lang), show_alert=True)
        return

    stars = settings.price_protection_stars
    payment = await sub_svc.create_payment(
        session,
        user_id=call.from_user.id,
        plan=None,
        method=PaymentMethod.STARS,
        amount_stars=stars,
        product="protection",
    )

    await call.message.answer_invoice(
        title=t("protection_invoice_title", lang),
        description=t("protection_invoice_desc", lang),
        payload=str(payment.id),
        currency="XTR",
        prices=[LabeledPrice(label="Stars", amount=stars)],
    )
    await call.answer()


@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_stars_payment(message: Message, session: AsyncSession):
    payload = message.successful_payment.invoice_payload
    from sqlalchemy import select
    from db.models import Payment
    result = await session.execute(select(Payment).where(Payment.id == int(payload)))
    payment = result.scalar_one_or_none()
    if not payment:
        return

    user = await sub_svc.get_user(session, message.from_user.id)
    lang = _lang(user)

    if payment.product == "protection":
        await sub_svc.confirm_protection_payment(session, payment.id)
        await message.answer(
            t("protection_activated", lang),
            reply_markup=back_main_kb(lang),
            parse_mode="HTML",
        )
        return

    sub, _ = await sub_svc.confirm_payment(session, payment.id)
    expires = sub.expires_at.strftime("%d.%m.%Y")
    await message.answer(
        f"<b>Оплата звёздами подтверждена.</b>\n\n"
        f"Подписка активна до <b>{expires}</b>.\n\n"
        f"Подключи бота: Настройки → Автоматизация чатов → Чат-боты",
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
