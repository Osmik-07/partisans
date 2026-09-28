"""
Platega webhook handler (СБП).
Подключается к основному aiohttp app так же, как CryptoBot webhook.
"""
import logging

from aiohttp import web

from bot.services import platega as platega_svc
from bot.services import subscription as sub_svc
from db.base import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def platega_webhook_handler(request: web.Request) -> web.Response:
    body = await request.read()

    # При сохранении Callback URL в ЛК Platega шлёт пустой POST для проверки
    # валидности адреса — на него достаточно ответить 200 OK, до заголовков
    # авторизации дело не доходит.
    if not body:
        return web.Response(text="ok")

    try:
        data = await request.json()
    except Exception:
        return web.Response(status=400, text="Bad JSON")

    if not platega_svc.verify_webhook_headers(request.headers):
        logger.warning("Platega webhook: invalid X-MerchantId/X-Secret")
        return web.Response(status=401, text="Invalid credentials")

    status = data.get("status")
    external_id = str(data.get("id") or "")
    payload_raw = str(data.get("payload") or "")

    logger.info(f"Platega callback: id={external_id} status={status} payload={payload_raw}")

    if status != "CONFIRMED":
        return web.Response(text="ok")

    try:
        async with AsyncSessionLocal() as session:
            payment = await sub_svc.get_payment_by_external_id(session, external_id)
            if not payment and payload_raw.isdigit():
                from sqlalchemy import select
                from db.models import Payment
                result = await session.execute(
                    select(Payment).where(Payment.id == int(payload_raw))
                )
                payment = result.scalar_one_or_none()

            if not payment:
                logger.warning(f"Payment not found for Platega transaction {external_id}")
                return web.Response(text="ok")

            from db.models import PaymentStatus
            if payment.status == PaymentStatus.PAID:
                return web.Response(text="ok")  # уже обработан; callback может дублироваться

            is_protection = payment.product == "protection"
            user_id = payment.user_id

            if is_protection:
                created = await sub_svc.confirm_protection_payment(session, payment.id)
            else:
                sub, created = await sub_svc.confirm_payment(session, payment.id)
                expires = sub.expires_at.strftime("%d.%m.%Y") if sub else None

            async with AsyncSessionLocal() as lang_session:
                from db.models import User
                owner = await lang_session.get(User, user_id)
                lang = owner.lang if owner and owner.lang else "en"

        if not created:
            return web.Response(text="ok")

        bot = request.app["bot"]
        if is_protection:
            from bot.i18n import t
            await bot.send_message(user_id, t("protection_activated", lang), parse_mode="HTML")
        else:
            await bot.send_message(
                user_id,
                f"<b>Оплата подтверждена.</b>\n\n"
                f"Подписка активна до <b>{expires}</b>.\n\n"
                f"Подключи бота: Настройки → Автоматизация чатов → Чат-боты",
                parse_mode="HTML",
            )
    except Exception as e:
        logger.exception(f"Platega webhook error: {e}")

    return web.Response(text="ok")


def register_platega_webhook(app: web.Application):
    app.router.add_post("/platega/webhook", platega_webhook_handler)
