"""add_username

Revision ID: e3690935f6c5
Revises: 6067e130dc7b
Create Date: 2021-10-30 20:06:02.112267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3690935f6c5'
down_revision = '6067e130dc7b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users_chat', sa.Column('user_name', sa.String ,nullable=True))


def downgrade():
    op.drop_column('users_chat', 'user_name')

