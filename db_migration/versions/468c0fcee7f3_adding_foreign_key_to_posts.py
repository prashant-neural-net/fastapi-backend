"""adding foreign key to posts

Revision ID: 468c0fcee7f3
Revises: 311f11518f5e
Create Date: 2026-08-12 00:19:08.448930

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "468c0fcee7f3"
down_revision: Union[str, Sequence[str], None] = "311f11518f5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", "posts")
    op.drop_column("posts", "user_id")
    pass
