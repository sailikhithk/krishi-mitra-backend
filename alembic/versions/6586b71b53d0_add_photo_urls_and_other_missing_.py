"""Add photo_urls and other missing columns to produce_listings

Revision ID: 6586b71b53d0
Revises: 0a2b73b18c72
Create Date: 2024-10-14 08:09:14.574774

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6586b71b53d0"
down_revision: Union[str, None] = "0a2b73b18c72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add photo_urls column to produce_listings table
    op.add_column(
        "produce_listings", sa.Column("photo_urls", sa.String(), nullable=True)
    )
    # Add any other missing columns here as needed


def downgrade():
    # Remove photo_urls column from produce_listings table
    op.drop_column("produce_listings", "photo_urls")
