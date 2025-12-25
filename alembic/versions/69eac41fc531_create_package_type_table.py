"""create package type  table

Revision ID: 69eac41fc531
Revises: 6810c934a22f
Create Date: 2025-12-25 15:31:28.445281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69eac41fc531'
down_revision: Union[str, Sequence[str], None] = '6810c934a22f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'pkg_type',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer, sa.ForeignKey('organization.id'), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('updated_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('is_deleted', sa.Boolean, server_default=sa.text('false'))
    )

    op.create_index(
    'ux_pkg_type_org_name',
    'pkg_type',
    ['org_id', 'name'],
    unique=True,
    postgresql_where=sa.text('is_deleted = FALSE')
)


def downgrade() -> None:
    op.drop_table('pkg_type')
