"""add reminded_24h_at to subscriptions

Revision ID: 20260422_subscription_reminders
Revises: 20260416_saved_messages_ttl
Create Date: 2026-04-22
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260422_subscription_reminders"
down_revision: Union[str, None] = "20260416_saved_messages_ttl"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "subscriptions",
        sa.Column("reminded_24h_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_subscriptions_reminded_24h_at",
        "subscriptions",
        ["reminded_24h_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_subscriptions_reminded_24h_at", table_name="subscriptions")
    op.drop_column("subscriptions", "reminded_24h_at")
