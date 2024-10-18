"""Add delivery_photo_url and other missing columns to logistics

Revision ID: 74a14b10a63b
Revises: 1b3a9ec1ca46
Create Date: 2024-10-14 10:24:37.823473

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "74a14b10a63b"
down_revision: Union[str, None] = "1b3a9ec1ca46"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add delivery_photo_url column to logistics table
    op.add_column(
        "logistics", sa.Column("delivery_photo_url", sa.String(), nullable=True)
    )
    # Add any other missing columns here as needed


def downgrade():
    # Remove delivery_photo_url column from logistics table
    op.drop_column("logistics", "delivery_photo_url")
