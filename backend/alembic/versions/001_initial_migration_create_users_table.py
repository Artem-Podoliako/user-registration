"""Initial migration: create users table

Revision ID: 001
Revises: 
Create Date: 2025-12-19 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login', sa.String(length=32), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login', name='uq_users_login')
    )
    # Create index on id
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    # Create unique index on login
    op.create_index('ix_users_login', 'users', ['login'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_users_login', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    # Drop table
    op.drop_table('users')

