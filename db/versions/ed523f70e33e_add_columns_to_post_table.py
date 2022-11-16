"""add columns to post table

Revision ID: ed523f70e33e
Revises: 20a281d2450a
Create Date: 2022-11-16 10:43:02.829691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed523f70e33e'
down_revision = '20a281d2450a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='true'))
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))

    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
