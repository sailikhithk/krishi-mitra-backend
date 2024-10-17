"""Add acceptance_status and other missing columns to bids

Revision ID: 50abc0b8dbd7
Revises: c76282fe9ffd
Create Date: 2024-10-14 10:03:13.427921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '50abc0b8dbd7'
down_revision: Union[str, None] = 'c76282fe9ffd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add acceptance_status column to bids table
    op.add_column('bids', sa.Column('acceptance_status', sa.String(), nullable=True))
    # Add any other missing columns here as needed

def downgrade():
    # Remove acceptance_status column from bids table
    op.drop_column('bids', 'acceptance_status')