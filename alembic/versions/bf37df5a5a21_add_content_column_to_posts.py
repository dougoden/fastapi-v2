"""Add content column to posts

Revision ID: bf37df5a5a21
Revises: a1c1c290f5a9
Create Date: 2023-07-09 18:32:08.140941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bf37df5a5a21"
down_revision = "a1c1c290f5a9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
