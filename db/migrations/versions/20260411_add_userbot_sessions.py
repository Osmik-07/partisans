"""add userbot sessions table

Revision ID: 20260411_add_userbot_sessions
Revises: None
Create Date: 2026-04-11 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260411_add_userbot_sessions"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    subscription_plan = sa.Enum("trial", "week", "month", "year", name="subscriptionplan")
    payment_method = sa.Enum("cryptobot", "stars", name="paymentmethod")
    payment_status = sa.Enum("pending", "paid", "expired", "cancelled", name="paymentstatus")
    message_type = sa.Enum("deleted", "edited", "vanishing_photo", name="messagetype")

    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=128), nullable=True),
        sa.Column("language_code", sa.String(length=8), nullable=True),
        sa.Column("is_banned", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("trial_used", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("business_connection_id", sa.String(length=256), nullable=True),
        sa.Column("business_connected_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("plan", subscription_plan, nullable=False),
        sa.Column("method", payment_method, nullable=False),
        sa.Column("status", payment_status, nullable=False, server_default=sa.text("'pending'")),
        sa.Column("amount_usd", sa.Float(), nullable=True),
        sa.Column("amount_stars", sa.Integer(), nullable=True),
        sa.Column("external_id", sa.String(length=256), nullable=True),
        sa.Column("invoice_url", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("plan", subscription_plan, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payment_id", sa.Integer(), sa.ForeignKey("payments.id"), nullable=True),
    )

    op.create_table(
        "saved_messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("owner_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("message_type", message_type, nullable=False),
        sa.Column("from_user_id", sa.BigInteger(), nullable=True),
        sa.Column("from_username", sa.String(length=64), nullable=True),
        sa.Column("from_first_name", sa.String(length=128), nullable=True),
        sa.Column("chat_id", sa.BigInteger(), nullable=True),
        sa.Column("message_id", sa.BigInteger(), nullable=True),
        sa.Column("business_connection_id", sa.String(length=256), nullable=True),
        sa.Column("original_text", sa.Text(), nullable=True),
        sa.Column("new_text", sa.Text(), nullable=True),
        sa.Column("media_file_id", sa.String(length=512), nullable=True),
        sa.Column("media_type", sa.String(length=32), nullable=True),
        sa.Column("extra_data", sa.JSON(), nullable=True),
        sa.Column("event_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("notified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    op.create_table(
        "userbot_sessions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("session_string", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("last_active", sa.DateTime(timezone=True), nullable=True),
        sa.Column("auth_data", sa.JSON(), nullable=True),
    )
    op.create_index(
        "ix_userbot_sessions_user_id",
        "userbot_sessions",
        ["user_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_userbot_sessions_user_id", table_name="userbot_sessions")
    op.drop_table("userbot_sessions")
    op.drop_table("saved_messages")
    op.drop_table("subscriptions")
    op.drop_table("payments")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS messagetype")
    op.execute("DROP TYPE IF EXISTS paymentstatus")
    op.execute("DROP TYPE IF EXISTS paymentmethod")
    op.execute("DROP TYPE IF EXISTS subscriptionplan")
