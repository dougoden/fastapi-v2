"""Add foreign key to posts

Revision ID: 70cd57217c85
Revises: abb4f4c80101
Create Date: 2023-07-12 19:14:05.944916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "70cd57217c85"
down_revision = "abb4f4c80101"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
