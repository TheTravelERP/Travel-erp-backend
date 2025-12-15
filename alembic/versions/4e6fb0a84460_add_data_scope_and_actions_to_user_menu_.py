"""add data_scope and actions to user_menu_permission

Revision ID: 4e6fb0a84460
Revises: ae70799d2c23
Create Date: 2025-12-15 19:03:50.693514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e6fb0a84460'
down_revision: Union[str, Sequence[str], None] = 'ae70799d2c23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    data_scope_enum = sa.Enum(
        "OWN", "TEAM", "ORG", "GLOBAL",
        name="data_scope_enum"
    )
    data_scope_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "user_menu_permission",
        sa.Column("can_import", sa.Boolean(), nullable=False, server_default=sa.false())
    )
    op.add_column(
        "user_menu_permission",
        sa.Column("can_print", sa.Boolean(), nullable=False, server_default=sa.false())
    )
    op.add_column(
        "user_menu_permission",
        sa.Column("data_scope", data_scope_enum, nullable=False, server_default="OWN")
    )

    op.alter_column("user_menu_permission", "can_import", server_default=None)
    op.alter_column("user_menu_permission", "can_print", server_default=None)
    op.alter_column("user_menu_permission", "data_scope", server_default=None)





def downgrade() -> None:
    op.drop_column("user_menu_permission", "data_scope")
    op.drop_column("user_menu_permission", "can_print")
    op.drop_column("user_menu_permission", "can_import")

    sa.Enum(name="data_scope_enum").drop(op.get_bind(), checkfirst=True)
