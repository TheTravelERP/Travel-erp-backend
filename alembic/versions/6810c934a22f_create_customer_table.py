"""create customer table

Revision ID: 6810c934a22f
Revises: 4e6fb0a84460
Create Date: 2025-12-25 15:29:19.002189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6810c934a22f'
down_revision: Union[str, Sequence[str], None] = '4e6fb0a84460'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'customer',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer, sa.ForeignKey('organization.id'), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('passport_no', sa.String(50)),
        sa.Column('email', sa.String(200)),
        sa.Column('mobile', sa.String(20)),
        sa.Column('gstin', sa.String(20)),
        sa.Column('billing_address', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('updated_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('is_deleted', sa.Boolean, server_default=sa.text('false'))
    )

    op.create_index(
        'ux_customer_email',
        'customer',
        ['org_id', 'email'],
        unique=True,
        postgresql_where=sa.text('email IS NOT NULL AND is_deleted = FALSE')
    )



def downgrade() -> None:
    op.drop_table('customer')
