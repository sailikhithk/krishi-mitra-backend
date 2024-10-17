"""Add phone_number and rating columns to users table

Revision ID: c92de5265454
Revises: 183fc480fd37
Create Date: 2024-10-13 09:15:26.698613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c92de5265454'
down_revision: Union[str, None] = '183fc480fd37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('rating', sa.Float(), nullable=True))



def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'rating')
