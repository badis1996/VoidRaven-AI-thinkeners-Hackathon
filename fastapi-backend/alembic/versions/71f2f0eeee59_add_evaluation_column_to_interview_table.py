"""add evaluation column to interview table

Revision ID: 71f2f0eeee59
Revises: 001
Create Date: 2025-02-16 15:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '71f2f0eeee59'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add evaluation column to interview table
    op.add_column('interview', sa.Column('evaluation', postgresql.JSON(), nullable=True))


def downgrade() -> None:
    # Remove evaluation column from interview table
    op.drop_column('interview', 'evaluation')
