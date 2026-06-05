"""add referral program support

Revision ID: 20260516_referral_program
Revises: 20260422_subscription_reminders
Create Date: 2026-05-16 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260516_referral_program"
down_revision: Union[str, None] = "20260422_subscription_reminders"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE subscriptionplan ADD VALUE IF NOT EXISTS 'bonus'")

    op.add_column("users", sa.Column("referred_by_id", sa.BigInteger(), nullable=True))
    op.create_foreign_key(
        "fk_users_referred_by_id_users",
        "users",
        "users",
        ["referred_by_id"],
        ["id"],
    )

    op.create_table(
        "referral_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("referrer_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("invited_user_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("bonus_days", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("invited_user_id", name="uq_referral_events_invited_user_id"),
    )


def downgrade() -> None:
    op.drop_table("referral_events")
    op.drop_constraint("fk_users_referred_by_id_users", "users", type_="foreignkey")
    op.drop_column("users", "referred_by_id")
