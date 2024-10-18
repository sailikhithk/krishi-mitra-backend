"""Add delivery_address and other missing columns to bids

Revision ID: 6384cfe59672
Revises: c841afafa87e
Create Date: 2024-10-14 10:20:42.323878

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6384cfe59672"
down_revision: Union[str, None] = "c841afafa87e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add delivery_address column to bids table
    op.add_column("bids", sa.Column("delivery_address", sa.String(), nullable=True))
    # Add any other missing columns here as needed


def downgrade():
    # Remove delivery_address column from bids table
    op.drop_column("bids", "delivery_address")
