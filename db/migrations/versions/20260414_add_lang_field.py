"""add lang field

Revision ID: 20260414_add_lang_field
Revises: 20260411_add_userbot_sessions
Create Date: 2026-04-14 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260414_add_lang_field"
down_revision: Union[str, None] = "20260411_add_userbot_sessions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("lang", sa.String(length=10), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "lang")