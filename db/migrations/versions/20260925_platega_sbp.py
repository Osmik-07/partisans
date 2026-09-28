"""add platega payment method (amount_rub, paymentmethod.platega)

Revision ID: 20260925_platega_sbp
Revises: 20260906_protection
Create Date: 2026-09-25 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260925_platega_sbp"
down_revision: Union[str, None] = "20260906_protection"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Postgres allows ADD VALUE inside a transaction since PG12 (this project runs
    # postgres:16-alpine); the new value just can't be used in the SAME transaction
    # it was added in — fine here, this migration is DDL-only.
    op.execute("ALTER TYPE paymentmethod ADD VALUE IF NOT EXISTS 'platega'")
    op.add_column(
        "payments",
        sa.Column("amount_rub", sa.Float(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("payments", "amount_rub")
    # Postgres has no ALTER TYPE ... DROP VALUE — the 'platega' enum label stays,
    # it's just unused after downgrade.
