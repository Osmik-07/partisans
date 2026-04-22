from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlalchemy import (
    BigInteger, String, Boolean, DateTime, Integer,
    Float, ForeignKey, Enum, Text, JSON, LargeBinary
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SubscriptionPlan(str, PyEnum):
    TRIAL = "trial"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class PaymentMethod(str, PyEnum):
    CRYPTOBOT = "cryptobot"
    STARS = "stars"


class PaymentStatus(str, PyEnum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(64))
    first_name: Mapped[str | None] = mapped_column(String(128))
    language_code: Mapped[str | None] = mapped_column(String(8))
    lang: Mapped[str] = mapped_column(String(8), default="en")
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    trial_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    business_connection_id: Mapped[str | None] = mapped_column(String(256))
    business_connected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="user", lazy="selectin",
    )
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="user", lazy="noload"
    )
    saved_messages: Mapped[list["SavedMessage"]] = relationship(
        back_populates="user", lazy="noload"
    )
    # Сессия userbot — одна на пользователя
    userbot_session: Mapped["UserbotSession | None"] = relationship(
        back_populates="user", lazy="noload", uselist=False
    )

    @property
    def active_subscription(self) -> "Subscription | None":
        now = utcnow()
        active = [
            sub for sub in self.subscriptions
            if sub.is_active and sub.expires_at > now
        ]
        if not active:
            return None
        return max(active, key=lambda sub: sub.expires_at)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    plan: Mapped[SubscriptionPlan] = mapped_column(Enum(SubscriptionPlan))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    payment_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("payments.id"))
    reminded_24h_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="subscriptions")
    payment: Mapped["Payment | None"] = relationship(foreign_keys=[payment_id])


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    plan: Mapped[SubscriptionPlan] = mapped_column(Enum(SubscriptionPlan))
    method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod))
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    amount_usd: Mapped[float | None] = mapped_column(Float)
    amount_stars: Mapped[int | None] = mapped_column(Integer)

    external_id: Mapped[str | None] = mapped_column(String(256))
    invoice_url: Mapped[str | None] = mapped_column(String(512))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="payments")


class MessageType(str, PyEnum):
    DELETED = "deleted"
    EDITED = "edited"
    VANISHING_PHOTO = "vanishing_photo"


class SavedMessage(Base):
    __tablename__ = "saved_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    message_type: Mapped[MessageType] = mapped_column(Enum(MessageType))

    from_user_id: Mapped[int | None] = mapped_column(BigInteger)
    from_username: Mapped[str | None] = mapped_column(String(64))
    from_first_name: Mapped[str | None] = mapped_column(String(128))
    chat_id: Mapped[int | None] = mapped_column(BigInteger)
    message_id: Mapped[int | None] = mapped_column(BigInteger)
    business_connection_id: Mapped[str | None] = mapped_column(String(256))

    original_text: Mapped[str | None] = mapped_column(Text)
    new_text: Mapped[str | None] = mapped_column(Text)
    media_file_id: Mapped[str | None] = mapped_column(String(512))
    media_type: Mapped[str | None] = mapped_column(String(32))
    extra_data: Mapped[dict | None] = mapped_column(JSON)

    event_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    notified: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="saved_messages")


class UserbotSession(Base):
    """Хранит Pyrogram сессию пользователя в БД."""
    __tablename__ = "userbot_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True)

    phone: Mapped[str | None] = mapped_column(String(32))
    # Строка сессии Pyrogram (StringSession)
    session_string: Mapped[str | None] = mapped_column(Text)

    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_active: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Временные данные для процесса авторизации (phone_code_hash)
    auth_data: Mapped[dict | None] = mapped_column(JSON)

    user: Mapped["User"] = relationship(back_populates="userbot_session")
