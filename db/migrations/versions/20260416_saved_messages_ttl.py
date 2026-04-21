"""add expires_at to saved_messages

Revision ID: 20260416_saved_messages_ttl
Revises: 20260414_add_lang_field
Create Date: 2026-04-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "20260416_saved_messages_ttl"
down_revision: Union[str, None] = "20260414_add_lang_field"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "saved_messages",
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_saved_messages_expires_at",
        "saved_messages",
        ["expires_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_saved_messages_expires_at", table_name="saved_messages")
    op.drop_column("saved_messages", "expires_at")