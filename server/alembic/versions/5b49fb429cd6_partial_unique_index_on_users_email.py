"""partial unique index on users email

Revision ID: 5b49fb429cd6
Revises: fa7ea08c06ba
Create Date: 2026-09-03 22:05:07.857277

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "5b49fb429cd6"
down_revision: Union[str, Sequence[str], None] = "fa7ea08c06ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.create_index(
        "ix_users_email_unique_active",
        "users",
        ["email"],
        unique=True,
        postgresql_where=sa.text("is_deleted = false"),
    )


def downgrade() -> None:
    op.drop_index("ix_users_email_unique_active", table_name="users")
    op.create_index("ix_users_email", "users", ["email"], unique=True)
