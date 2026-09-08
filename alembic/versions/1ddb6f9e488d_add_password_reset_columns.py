"""add password reset columns

Revision ID: 1ddb6f9e488d
Revises: 9f7b87dcaa30
Create Date: 2026-09-08 21:01:26.207442

Adds users.reset_token and users.reset_token_expires.

Deliberately uses plain add_column/create_index rather than
batch_alter_table. SQLite supports ALTER TABLE ADD COLUMN natively for
nullable columns, so no table is rebuilt and existing rows are untouched.

Autogenerate also proposed rebuilding `documents` (adding a foreign key on
conversation_id and making created_at NOT NULL) and `github_connections`
(NOT NULL on id, plus an index). Those are pre-existing drift between the
models and a database that predates Alembic -- unrelated to password reset,
and each would rebuild a table holding live rows. They are left out of this
migration and should be addressed by their own reviewed revision.
"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1ddb6f9e488d'
down_revision: Union[str, Sequence[str], None] = '9f7b87dcaa30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the password reset columns."""
    op.add_column(
        "users",
        sa.Column("reset_token", sa.String(), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("reset_token_expires", sa.DateTime(), nullable=True),
    )
    op.create_index(
        op.f("ix_users_reset_token"),
        "users",
        ["reset_token"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the password reset columns."""
    op.drop_index(op.f("ix_users_reset_token"), table_name="users")
    op.drop_column("users", "reset_token_expires")
    op.drop_column("users", "reset_token")
