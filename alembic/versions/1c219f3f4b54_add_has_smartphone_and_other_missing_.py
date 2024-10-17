"""Add has_smartphone and other missing columns to logistics

Revision ID: 1c219f3f4b54
Revises: 74a14b10a63b
Create Date: 2024-10-14 11:20:06.626256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1c219f3f4b54'
down_revision: Union[str, None] = '74a14b10a63b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add has_smartphone column to logistics table
    op.add_column('logistics', sa.Column('has_smartphone', sa.Boolean(), nullable=True))
    # Add any other missing columns here as needed

def downgrade():
    # Remove has_smartphone column from logistics table
    op.drop_column('logistics', 'has_smartphone')