"""create city_master and menu_master

Revision ID: 86c3712408d7
Revises: afd56bc700df
Create Date: 2025-12-15 15:15:25.780970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86c3712408d7'
down_revision: Union[str, Sequence[str], None] = 'afd56bc700df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "city_master",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("country_code", sa.String(2), nullable=False),
        sa.Column("city_code", sa.String(10), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "menu_master",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(100), nullable=False, unique=True),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("path", sa.String(255), nullable=True),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("menu_master.id")),
        sa.Column("sort_order", sa.Integer(), default=0),
        sa.Column("is_active", sa.Boolean(), default=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("menu_master")
    op.drop_table("city_master")
