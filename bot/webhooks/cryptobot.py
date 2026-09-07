"""
CryptoBot webhook handler.
Подключается к основному aiohttp app при работе в webhook-режиме.
При polling — запускается отдельным маршрутом через aiohttp.
"""
import json
import hashlib
import hmac
import logging

from aiohttp import web
from bot.config import settings
from bot.services import cryptobot as crypto_svc
from bot.services import subscription as sub_svc
from db.base import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def cryptobot_webhook_handler(request: web.Request) -> web.Response:
    body = await request.read()
    signature = request.headers.get("crypto-pay-api-signature", "")

    if not crypto_svc.verify_webhook(body, signature):
        logger.warning("CryptoBot webhook: invalid signature")
        return web.Response(status=403, text="Invalid signature")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return web.Response(status=400, text="Bad JSON")

    update_type = data.get("update_type")
    if update_type != "invoice_paid":
        return web.Response(text="ok")

    payload_obj = data.get("payload", {})
    if isinstance(payload_obj, dict):
        invoice_id = str(payload_obj.get("invoice_id") or data.get("invoice_id") or "")
        invoice_payload = str(payload_obj.get("payload") or payload_obj.get("invoice_payload") or "")
    else:
        invoice_id = str(data.get("invoice_id") or "")
        invoice_payload = str(payload_obj or "")

    logger.info(f"CryptoBot paid: invoice_id={invoice_id} payload={invoice_payload}")

    try:
        async with AsyncSessionLocal() as session:
            payment = await sub_svc.get_payment_by_external_id(session, invoice_id)
            if not payment:
                # Ищем по payload (payment.id)
                from sqlalchemy import select
                from db.models import Payment
                result = await session.execute(
                    select(Payment).where(Payment.id == int(invoice_payload))
                )
                payment = result.scalar_one_or_none()

            if not payment:
                logger.warning(f"Payment not found: {invoice_id}")
                return web.Response(text="ok")

            from db.models import PaymentStatus
            if payment.status == PaymentStatus.PAID:
                return web.Response(text="ok")  # уже обработан

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

        # Уведомляем пользователя
        if not created:
            return web.Response(text="ok")

        bot = request.app["bot"]
        if is_protection:
            from bot.i18n import t
            await bot.send_message(
                user_id,
                t("protection_activated", lang),
                parse_mode="HTML",
            )
        else:
            await bot.send_message(
                user_id,
                f"<b>Оплата подтверждена.</b>\n\n"
                f"Подписка активна до <b>{expires}</b>.\n\n"
                f"Подключи бота: Настройки → Автоматизация чатов → Чат-боты",
                parse_mode="HTML",
            )
    except Exception as e:
        logger.exception(f"CryptoBot webhook error: {e}")

    return web.Response(text="ok")


def register_cryptobot_webhook(app: web.Application):
    app.router.add_post("/cryptobot/webhook", cryptobot_webhook_handler)
