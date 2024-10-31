"""Add govt_price and other missing columns to produce_listings

Revision ID: 0a2b73b18c72
Revises: 85e7671293ec
Create Date: 2024-10-14 07:35:57.182300

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0a2b73b18c72"
down_revision: Union[str, None] = "85e7671293ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add govt_price column to produce_listings table
    op.add_column(
        "produce_listings", sa.Column("govt_price", sa.Float(), nullable=True)
    )
    # Add any other missing columns here as needed


def downgrade():
    # Remove govt_price column from produce_listings table
    op.drop_column("produce_listings", "govt_price")
