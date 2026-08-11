"""add new column- content to posts table

Revision ID: 8a3a5dd9174f
Revises: 516420c07d5b
Create Date: 2026-08-11 23:38:56.391906

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8a3a5dd9174f"
down_revision: Union[str, Sequence[str], None] = "516420c07d5b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.TEXT(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
