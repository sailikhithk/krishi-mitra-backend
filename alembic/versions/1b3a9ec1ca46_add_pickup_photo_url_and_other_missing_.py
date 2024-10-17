"""Add pickup_photo_url and other missing columns to logistics

Revision ID: 1b3a9ec1ca46
Revises: 6384cfe59672
Create Date: 2024-10-14 10:23:17.965618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1b3a9ec1ca46'
down_revision: Union[str, None] = '6384cfe59672'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add pickup_photo_url column to logistics table
    op.add_column('logistics', sa.Column('pickup_photo_url', sa.String(), nullable=True))
    # Add any other missing columns here as needed

def downgrade():
    # Remove pickup_photo_url column from logistics table
    op.drop_column('logistics', 'pickup_photo_url')