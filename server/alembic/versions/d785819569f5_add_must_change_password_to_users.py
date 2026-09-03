"""add must_change_password to users

Revision ID: d785819569f5
Revises: 172f66790327
Create Date: 2026-08-29 21:21:32.380612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "d785819569f5"
down_revision: Union[str, Sequence[str], None] = "172f66790327"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "must_change_password",
            sa.Boolean(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "must_change_password")
