"""add protection product (protected_users, interception_attempts, payments.product)

Revision ID: 20260906_protection
Revises: 20260905_terms_accepted
Create Date: 2026-09-06 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260906_protection"
down_revision: Union[str, None] = "20260905_terms_accepted"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "payments",
        sa.Column("product", sa.String(length=32), nullable=False, server_default="subscription"),
    )
    op.alter_column(
        "payments",
        "plan",
        existing_type=postgresql.ENUM(name="subscriptionplan", create_type=False),
        nullable=True,
    )

    op.create_table(
        "protected_users",
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("payment_id", sa.Integer(), sa.ForeignKey("payments.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "interception_attempts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("protected_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("from_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index(
        "ix_interception_attempts_protected_id",
        "interception_attempts",
        ["protected_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_interception_attempts_protected_id", table_name="interception_attempts")
    op.drop_table("interception_attempts")
    op.drop_table("protected_users")
    op.alter_column(
        "payments",
        "plan",
        existing_type=postgresql.ENUM(name="subscriptionplan", create_type=False),
        nullable=False,
    )
    op.drop_column("payments", "product")
