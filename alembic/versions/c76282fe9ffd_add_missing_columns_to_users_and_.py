"""Add missing columns to users and produce_listings

Revision ID: c76282fe9ffd
Revises: 93d6f77f7c1a
Create Date: 2024-10-14 09:33:38.729877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c76282fe9ffd'
down_revision: Union[str, None] = '93d6f77f7c1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add missing columns to users table
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('rating', sa.Float(), nullable=True))
    # Add any other missing columns here as needed

    # Add missing columns to produce_listings table
    op.add_column('produce_listings', sa.Column('category', sa.Enum('daily', 'weekly_monthly', 'dry_spices_nuts', 'grains', name='producecategory'), nullable=True))
    op.add_column('produce_listings', sa.Column('minimum_bid_price', sa.Float(), nullable=True))
    op.add_column('produce_listings', sa.Column('govt_price', sa.Float(), nullable=True))
    op.add_column('produce_listings', sa.Column('photo_urls', sa.String(), nullable=True))
    op.add_column('produce_listings', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('produce_listings', sa.Column('pickup_location', sa.String(), nullable=True))
    op.add_column('produce_listings', sa.Column('distance', sa.Float(), nullable=True))

def downgrade():
    # Remove added columns from users table
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'rating')

    # Remove added columns from produce_listings table
    op.drop_column('produce_listings', 'category')
    op.drop_column('produce_listings', 'minimum_bid_price')
    op.drop_column('produce_listings', 'govt_price')
    op.drop_column('produce_listings', 'photo_urls')
    op.drop_column('produce_listings', 'description')
    op.drop_column('produce_listings', 'pickup_location')
    op.drop_column('produce_listings', 'distance')