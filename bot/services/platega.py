"""
Клиент Platega API (СБП): https://docs.platega.io/

Используем «классическую пейформу» (paymentMethod=2, эндпоинт без /v2/), а не
универсальную: пользователь уже выбрал способ оплаты у нас в боте, и на самой
странице Platega ему незачем повторно выбирать между СБП/картой/крипто —
это развело бы платежи по методам, которые бот не отслеживает.

Выводы на карту и подписи PG-HMAC сюда не входят — это отдельная функция
личного кабинета мерчанта, бот её не использует.
"""
import aiohttp

from bot.config import settings

PLATEGA_API = "https://app.platega.io"
PAYMENT_METHOD_SBP = 2


def gross_up_for_display_price(display_price: float) -> float:
    """Сумма, которую нужно отправить в paymentDetails.amount, чтобы итоговый
    счёт (с комиссией Platega, добавляемой ими сверху) совпал с display_price —
    то есть с ценой, которую бот показывает в меню.

    Комиссия — процент от отправленной базы, округляется до копеек:
        comission = round(base * rate, 2)
        итог      = base + comission
    Проверено вживую 28.09.2026 на реальном мерчант-аккаунте: при рейте 8.5%
    база 91.24 → итог 99.00, база 137.33 → итог 149.00 — совпало день в день
    с формулой ниже, без единой копейки расхождения.

    Для «круглых» рублёвых цен (как у нас) обратный пересчёт обычно даёт точное
    совпадение, но при отправке дробь округляется дважды, поэтому теоретически
    возможно разойтись на 1 копейку — это неустранимое свойство округления,
    а не баг.
    """
    rate = settings.platega_sbp_commission_percent / 100
    return round(display_price / (1 + rate), 2)


def _headers() -> dict:
    return {
        "X-MerchantId": settings.platega_merchant_id,
        "X-Secret": settings.platega_secret,
        "Content-Type": "application/json",
    }


async def create_sbp_transaction(
    amount_rub: float,
    payload: str,
    description: str,
    return_url: str,
    failed_url: str,
) -> dict:
    """Создаёт транзакцию СБП и возвращает ответ Platega целиком:
    {transactionId, status, redirect, paymentDetails, expiresIn, ...}."""
    async with aiohttp.ClientSession() as session:
        resp = await session.post(
            f"{PLATEGA_API}/transaction/process",
            headers=_headers(),
            json={
                "paymentMethod": PAYMENT_METHOD_SBP,
                "paymentDetails": {"amount": amount_rub, "currency": "RUB"},
                "description": description,
                "return": return_url,
                "failedUrl": failed_url,
                "payload": payload,
            },
        )
        data = await resp.json()
    if resp.status != 200 or "transactionId" not in data:
        raise ValueError(f"Platega error: {data}")
    return data


async def get_transaction(transaction_id: str) -> dict:
    """Возвращает текущий статус и детали транзакции по её ID."""
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            f"{PLATEGA_API}/transaction/{transaction_id}",
            headers=_headers(),
        )
        data = await resp.json()
    if resp.status != 200:
        raise ValueError(f"Platega error: {data}")
    return data


def verify_webhook_headers(headers) -> bool:
    """Callback несёт ту же пару X-MerchantId/X-Secret, что и наши исходящие
    запросы — сверяем, чтобы отсечь поддельные уведомления."""
    if not settings.platega_merchant_id or not settings.platega_secret:
        return False
    return (
        headers.get("X-MerchantId", "") == settings.platega_merchant_id
        and headers.get("X-Secret", "") == settings.platega_secret
    )
