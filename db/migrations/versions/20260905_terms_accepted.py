"""add terms_accepted_at to userbot_sessions

Revision ID: 20260905_terms_accepted
Revises: 20260516_referral_program
Create Date: 2026-09-05 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260905_terms_accepted"
down_revision: Union[str, None] = "20260516_referral_program"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "userbot_sessions",
        sa.Column("terms_accepted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("userbot_sessions", "terms_accepted_at")
