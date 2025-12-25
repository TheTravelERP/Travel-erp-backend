"""create package table

Revision ID: 5f44c287fd4c
Revises: b34eda7519a1
Create Date: 2025-12-25 15:54:42.137984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f44c287fd4c'
down_revision: Union[str, Sequence[str], None] = 'b34eda7519a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'pkg',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer, sa.ForeignKey('organization.id'), nullable=False),
        sa.Column('pkg_type_id', sa.Integer, sa.ForeignKey('pkg_type.id')),
        sa.Column('pkg_detail_id', sa.Integer, sa.ForeignKey('pkg_detail.id')),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),

        sa.Column('total_seats', sa.Integer),
        sa.Column(
            'booked_seats',
            sa.Integer,
            server_default=sa.text('0')
        ),

        sa.Column('depart_date', sa.Date),
        sa.Column('arrive_date', sa.Date),
        sa.Column('depart_city', sa.String(100)),
        sa.Column('no_of_days', sa.Integer, sa.CheckConstraint('no_of_days > 0')),

        sa.Column('single_amt', sa.Numeric(14, 2)),
        sa.Column('currency_code', sa.String(3)),
        sa.Column('exchange_rate', sa.Numeric(18, 8)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('updated_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('is_deleted', sa.Boolean, server_default=sa.text('false')),
    )

    # Unique package code per org (ERP safe)
    op.create_index(
        'ux_pkg_code',
        'pkg',
        ['org_id', 'code'],
        unique=True,
        postgresql_where=sa.text('is_deleted = FALSE')
    )

    # Fast org-level queries
    op.create_index(
        'idx_pkg_org',
        'pkg',
        ['org_id']
    )


def downgrade() -> None:
    op.drop_table('pkg')
