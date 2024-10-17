"""Add phone_number to users table

Revision ID: 3710d6ff8d9e
Revises: 6a3d92dceef1
Create Date: 2024-10-13 09:05:01.986145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision: str = '3710d6ff8d9e'
down_revision: Union[str, None] = '6a3d92dceef1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add ProduceCategory enum if it doesn't exist
    produce_category = postgresql.ENUM('daily', 'weekly_monthly', 'dry_spices_nuts', 'grains', name='producecategory')
    produce_category.create(op.get_bind(), checkfirst=True)

    # Add new columns to users table
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('rating', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('farm_size', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('company_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('business_type', sa.String(), nullable=True))
    op.add_column('users', sa.Column('department', sa.String(), nullable=True))
    op.add_column('users', sa.Column('access_level', sa.String(), nullable=True))

    # Add new columns to bids table
    op.add_column('bids', sa.Column('acceptance_status', sa.String(), nullable=True))
    op.add_column('bids', sa.Column('rejection_reason', sa.String(), nullable=True))
    op.add_column('bids', sa.Column('delivery_address', sa.String(), nullable=True))

    # Add new columns to produce_listings table
    op.add_column('produce_listings', sa.Column('category', produce_category, nullable=True))
    op.add_column('produce_listings', sa.Column('minimum_bid_price', sa.Float(), nullable=True))
    op.add_column('produce_listings', sa.Column('govt_price', sa.Float(), nullable=True))
    op.add_column('produce_listings', sa.Column('photo_urls', sa.String(), nullable=True))
    op.add_column('produce_listings', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('produce_listings', sa.Column('pickup_location', sa.String(), nullable=True))
    op.add_column('produce_listings', sa.Column('distance', sa.Float(), nullable=True))

    # Add new columns to logistics table
    op.add_column('logistics', sa.Column('pickup_photo_url', sa.String(), nullable=True))
    op.add_column('logistics', sa.Column('delivery_photo_url', sa.String(), nullable=True))
    op.add_column('logistics', sa.Column('has_smartphone', sa.Boolean(), nullable=True))

def downgrade():
    # Remove added columns from users table
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'rating')
    op.drop_column('users', 'farm_size')
    op.drop_column('users', 'company_name')
    op.drop_column('users', 'business_type')
    op.drop_column('users', 'department')
    op.drop_column('users', 'access_level')

    # Remove added columns from bids table
    op.drop_column('bids', 'acceptance_status')
    op.drop_column('bids', 'rejection_reason')
    op.drop_column('bids', 'delivery_address')

    # Remove added columns from produce_listings table
    op.drop_column('produce_listings', 'category')
    op.drop_column('produce_listings', 'minimum_bid_price')
    op.drop_column('produce_listings', 'govt_price')
    op.drop_column('produce_listings', 'photo_urls')
    op.drop_column('produce_listings', 'description')
    op.drop_column('produce_listings', 'pickup_location')
    op.drop_column('produce_listings', 'distance')

    # Remove added columns from logistics table
    op.drop_column('logistics', 'pickup_photo_url')
    op.drop_column('logistics', 'delivery_photo_url')
    op.drop_column('logistics', 'has_smartphone')

    # Remove ProduceCategory enum
    produce_category = postgresql.ENUM('daily', 'weekly_monthly', 'dry_spices_nuts', 'grains', name='producecategory')
    produce_category.drop(op.get_bind(), checkfirst=True)