"""Add user table

Revision ID: abb4f4c80101
Revises: bf37df5a5a21
Create Date: 2023-07-12 19:04:18.520552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "abb4f4c80101"
down_revision = "bf37df5a5a21"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
