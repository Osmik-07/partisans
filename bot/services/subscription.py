from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from bot.config import settings
from db.models import User, Subscription, Payment, SubscriptionPlan, PaymentMethod, PaymentStatus


PLAN_DURATIONS = {
    SubscriptionPlan.TRIAL: timedelta(days=settings.price_trial_days),
    SubscriptionPlan.WEEK: timedelta(weeks=1),
    SubscriptionPlan.MONTH: timedelta(days=30),
    SubscriptionPlan.YEAR: timedelta(days=365),
}


async def get_or_create_user(session: AsyncSession, tg_user) -> User:
    user = await session.get(User, tg_user.id)
    if not user:
        user = User(
            id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            language_code=getattr(tg_user, "language_code", None),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    else:
        user.username = tg_user.username
        user.first_name = tg_user.first_name
        user.language_code = getattr(tg_user, "language_code", user.language_code)
        user.last_seen = datetime.now(timezone.utc)
        await session.commit()
    return user


async def get_user(
    session: AsyncSession,
    user_id: int,
    *,
    for_update: bool = False,
) -> User | None:
    query = (
        select(User)
        .options(selectinload(User.subscriptions))
        .where(User.id == user_id)
    )
    if for_update:
        query = query.with_for_update()

    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_active_subscription(
    session: AsyncSession,
    user_id: int,
) -> Subscription | None:
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(Subscription)
        .where(
            Subscription.user_id == user_id,
            Subscription.is_active == True,
            Subscription.expires_at > now,
        )
        .order_by(Subscription.expires_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def user_has_active_subscription(session: AsyncSession, user_id: int) -> bool:
    return await get_active_subscription(session, user_id) is not None


async def activate_subscription(
    session: AsyncSession,
    user_id: int,
    plan: SubscriptionPlan,
    payment: Payment | None = None,
) -> Subscription:
    now = datetime.now(timezone.utc)
    expires = now + PLAN_DURATIONS[plan]

    # Деактивируем старые
    await session.execute(
        update(Subscription)
        .where(Subscription.user_id == user_id, Subscription.is_active == True)
        .values(is_active=False)
    )

    sub = Subscription(
        user_id=user_id,
        plan=plan,
        is_active=True,
        started_at=now,
        expires_at=expires,
        payment_id=payment.id if payment else None,
        reminded_24h_at=None,
    )
    session.add(sub)

    if plan == SubscriptionPlan.TRIAL:
        await session.execute(
            update(User).where(User.id == user_id).values(trial_used=True)
        )

    await session.commit()
    await session.refresh(sub)
    return sub


async def create_payment(
    session: AsyncSession,
    user_id: int,
    plan: SubscriptionPlan,
    method: PaymentMethod,
    amount_usd: float | None = None,
    amount_stars: int | None = None,
) -> Payment:
    payment = Payment(
        user_id=user_id,
        plan=plan,
        method=method,
        status=PaymentStatus.PENDING,
        amount_usd=amount_usd,
        amount_stars=amount_stars,
    )
    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment


async def get_payment_by_external_id(session: AsyncSession, external_id: str) -> Payment | None:
    result = await session.execute(
        select(Payment).where(Payment.external_id == external_id)
    )
    return result.scalar_one_or_none()


async def confirm_payment(session: AsyncSession, payment_id: int) -> tuple[Subscription, bool]:
    result = await session.execute(
        select(Payment)
        .where(Payment.id == payment_id)
        .with_for_update()
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise ValueError(f"Payment {payment_id} not found")

    if payment.status == PaymentStatus.PAID:
        sub_result = await session.execute(
            select(Subscription)
            .where(Subscription.payment_id == payment.id)
            .order_by(Subscription.expires_at.desc())
            .limit(1)
        )
        existing_sub = sub_result.scalar_one_or_none()
        if existing_sub:
            return existing_sub, False

    now = datetime.now(timezone.utc)
    payment.status = PaymentStatus.PAID
    payment.paid_at = now

    await session.execute(
        update(Subscription)
        .where(Subscription.user_id == payment.user_id, Subscription.is_active == True)
        .values(is_active=False)
    )

    sub = Subscription(
        user_id=payment.user_id,
        plan=payment.plan,
        is_active=True,
        started_at=now,
        expires_at=now + PLAN_DURATIONS[payment.plan],
        payment_id=payment.id,
        reminded_24h_at=None,
    )
    session.add(sub)

    await session.commit()
    await session.refresh(sub)
    return sub, True


async def get_stats(session: AsyncSession) -> dict:
    from sqlalchemy import func
    total_users = (await session.execute(select(func.count(User.id)))).scalar()
    active_subs = (await session.execute(
        select(func.count(Subscription.id))
        .where(Subscription.is_active == True, Subscription.expires_at > datetime.now(timezone.utc))
    )).scalar()
    total_revenue = (await session.execute(
        select(func.sum(Payment.amount_usd))
        .where(Payment.status == PaymentStatus.PAID, Payment.amount_usd.isnot(None))
    )).scalar() or 0.0
    return {
        "total_users": total_users,
        "active_subs": active_subs,
        "total_revenue_usd": round(total_revenue, 2),
    }
# ── ADMIN: выдача подписки вручную ─────────────────────────

async def grant_subscription(
    session: AsyncSession,
    user_id: int,
    days: int,
    plan: SubscriptionPlan = SubscriptionPlan.MONTH,
) -> Subscription:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=days)

    # отключаем старые подписки
    await session.execute(
        update(Subscription)
        .where(
            Subscription.user_id == user_id,
            Subscription.is_active == True
        )
        .values(is_active=False)
    )

    sub = Subscription(
        user_id=user_id,
        plan=plan,
        is_active=True,
        started_at=now,
        expires_at=expires,
        payment_id=None,
        reminded_24h_at=None,
    )
    session.add(sub)

    await session.commit()
    await session.refresh(sub)
    return sub


async def activate_trial_subscription(session: AsyncSession, user_id: int) -> Subscription | None:
    user = await get_user(session, user_id, for_update=True)
    if not user or user.trial_used:
        return None

    return await activate_subscription(session, user_id, SubscriptionPlan.TRIAL)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    username = username.lstrip("@")

    result = await session.execute(
        select(User).where(User.username.ilike(username))
    )
    return result.scalar_one_or_none()
