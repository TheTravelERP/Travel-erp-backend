"""create user_menu_permission table

Revision ID: ae70799d2c23
Revises: 86c3712408d7
Create Date: 2025-12-15 16:35:00.831827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae70799d2c23'
down_revision: Union[str, Sequence[str], None] = '86c3712408d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user_menu_permission",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("menu_id", sa.Integer(), nullable=False),

        sa.Column("can_view", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("can_create", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("can_edit", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("can_delete", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("can_export", sa.Boolean(), nullable=False, server_default=sa.false()),

        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["menu_id"], ["menu_master.id"], ondelete="CASCADE"),

        sa.UniqueConstraint("user_id", "menu_id", name="uq_user_menu_permission"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_menu_permission")
