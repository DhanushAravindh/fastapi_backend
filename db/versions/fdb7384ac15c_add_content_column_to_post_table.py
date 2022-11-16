"""add content column to post table

Revision ID: fdb7384ac15c
Revises: c3c9b5664b8b
Create Date: 2022-11-16 10:20:55.896217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdb7384ac15c'
down_revision = 'c3c9b5664b8b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
