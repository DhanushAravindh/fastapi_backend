"""add foreign key to post table

Revision ID: 20a281d2450a
Revises: 2ce56f23b587
Create Date: 2022-11-16 10:35:50.745945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20a281d2450a'
down_revision = '2ce56f23b587'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_fk', source_table="posts", referent_table="users", local_cols={
                          'user_id'}, remote_cols={'id'}, ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
