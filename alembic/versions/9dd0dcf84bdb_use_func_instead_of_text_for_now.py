"""use func instead of text for now()

Revision ID: 9dd0dcf84bdb
Revises: 72302725cfa7
Create Date: 2023-07-29 15:47:56.757363

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = "9dd0dcf84bdb"
down_revision = "72302725cfa7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("posts", "created_at", server_default=func.now())


def downgrade() -> None:
    op.alter_column("posts", "created_at", server_default=sa.text("now()"))
