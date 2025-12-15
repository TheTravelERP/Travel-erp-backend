"""add org_code to organization

Revision ID: 2abb83f306af
Revises: 92b4cd0363ef
Create Date: 2025-12-15 12:11:13.806411

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2abb83f306af'
down_revision: Union[str, Sequence[str], None] = '92b4cd0363ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. add nullable column
    op.add_column(
        'organization',
        sa.Column('org_code', sa.String(length=20), nullable=True)
    )

    # 2. backfill existing orgs
    op.execute("""
        UPDATE organization
        SET org_code = 'ORG' || LPAD(id::text, 4, '0')
        WHERE org_code IS NULL
    """)

    # 3. enforce NOT NULL
    op.alter_column(
        'organization',
        'org_code',
        nullable=False
    )

    # 4. unique constraint
    op.create_unique_constraint(
        'uq_organization_org_code',
        'organization',
        ['org_code']
    )


def downgrade():
    op.drop_constraint('uq_organization_org_code', 'organization', type_='unique')
    op.drop_column('organization', 'org_code')

