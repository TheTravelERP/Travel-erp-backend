"""create enquiry table

Revision ID: 292ec2103bb3
Revises: 5f44c287fd4c
Create Date: 2025-12-25 16:13:55.350560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '292ec2103bb3'
down_revision: Union[str, Sequence[str], None] = '5f44c287fd4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'enquiry',
        sa.Column('id', sa.Integer, primary_key=True),

        # Multi-tenant
        sa.Column('org_id', sa.Integer, sa.ForeignKey('organization.id'), nullable=False),

        # Ownership
        sa.Column('agent_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('cust_id', sa.Integer, sa.ForeignKey('customer.id')),
        sa.Column('pkg_id', sa.Integer, sa.ForeignKey('pkg.id')),

        # Snapshot fields (ERP rule)
        sa.Column('customer_name', sa.String(200)),
        sa.Column('customer_mobile', sa.String(20)),
        sa.Column('customer_email', sa.String(200)),
        sa.Column('package_name', sa.String(200)),

        # Business data
        sa.Column('pax_count', sa.Integer, nullable=False),
        sa.Column('lead_source', sa.String(50), nullable=False),
        sa.Column('priority', sa.String(20), nullable=False),
        sa.Column('conversion_status', sa.String(20), nullable=False),
        sa.Column('description', sa.Text),

        # Financial (future use)
        sa.Column('quote_amount', sa.Numeric(14, 2)),
        sa.Column('currency_code', sa.String(3)),
        sa.Column('exchange_rate', sa.Numeric(18, 8)),

        # Audit
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('updated_by', sa.Integer, sa.ForeignKey('user.id')),

        sa.Column('is_deleted', sa.Boolean, server_default=sa.text('false')),

        # CHECK constraints
        sa.CheckConstraint('pax_count >= 1', name='ck_enquiry_pax_count'),
        sa.CheckConstraint(
            "priority IN ('Hot','Warm','Cold')",
            name='ck_enquiry_priority'
        ),
        sa.CheckConstraint(
            "conversion_status IN ('Lost','Pending','Converted')",
            name='ck_enquiry_conversion_status'
        ),
    )

    # Indexes (ERP-grade)
    op.create_index(
        'idx_enquiry_org',
        'enquiry',
        ['org_id'],
        postgresql_where=sa.text('is_deleted = FALSE')
    )

    op.create_index(
        'idx_enquiry_agent',
        'enquiry',
        ['agent_id'],
        postgresql_where=sa.text('is_deleted = FALSE')
    )

    op.create_index(
        'idx_enquiry_conversion',
        'enquiry',
        ['conversion_status'],
        postgresql_where=sa.text('is_deleted = FALSE')
    )


def downgrade() -> None:
    op.drop_index('idx_enquiry_conversion', table_name='enquiry')
    op.drop_index('idx_enquiry_agent', table_name='enquiry')
    op.drop_index('idx_enquiry_org', table_name='enquiry')
    op.drop_table('enquiry')