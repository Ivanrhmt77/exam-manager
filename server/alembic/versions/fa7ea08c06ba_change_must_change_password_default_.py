"""change must_change_password default value to true

Revision ID: fa7ea08c06ba
Revises: d785819569f5
Create Date: 2026-08-29 21:30:48.082021

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fa7ea08c06ba"
down_revision: Union[str, Sequence[str], None] = "d785819569f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "must_change_password",
        server_default=sa.text("true"),
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "must_change_password",
        server_default=None,
    )
