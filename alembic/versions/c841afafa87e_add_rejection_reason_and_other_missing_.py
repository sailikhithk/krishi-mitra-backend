"""Add rejection_reason and other missing columns to bids

Revision ID: c841afafa87e
Revises: 50abc0b8dbd7
Create Date: 2024-10-14 10:18:46.862226

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c841afafa87e"
down_revision: Union[str, None] = "50abc0b8dbd7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add rejection_reason column to bids table
    op.add_column("bids", sa.Column("rejection_reason", sa.String(), nullable=True))
    # Add any other missing columns here as needed


def downgrade():
    # Remove rejection_reason column from bids table
    op.drop_column("bids", "rejection_reason")
