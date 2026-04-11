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
    op.create_table(
        "userbot_sessions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
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
