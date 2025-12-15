"""add org_code as null to organization

Revision ID: afd56bc700df
Revises: 2abb83f306af
Create Date: 2025-12-15 14:37:36.845535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afd56bc700df'
down_revision: Union[str, Sequence[str], None] = '2abb83f306af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'organization',
        'org_code',
        existing_type=sa.String(length=10),
        nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'organization',
        'org_code',
        existing_type=sa.String(length=10),
        nullable=False
    )
