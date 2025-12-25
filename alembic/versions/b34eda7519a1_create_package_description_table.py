"""create package description table

Revision ID: b34eda7519a1
Revises: 69eac41fc531
Create Date: 2025-12-25 15:41:34.452549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b34eda7519a1'
down_revision: Union[str, Sequence[str], None] = '69eac41fc531'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'pkg_detail',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer, sa.ForeignKey('organization.id'), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('inclusive', sa.Text),
        sa.Column('exclusive', sa.Text),
        sa.Column('brochure_path', sa.String(500)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('updated_by', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('is_deleted', sa.Boolean, server_default=sa.text('false'))
    )


def downgrade() -> None:
     op.drop_table('pkg_detail')
