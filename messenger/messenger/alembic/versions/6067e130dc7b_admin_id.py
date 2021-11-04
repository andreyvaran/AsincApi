"""admin_id

Revision ID: 6067e130dc7b
Revises: 772194b1f5aa
Create Date: 2021-10-26 18:06:21.866785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '6067e130dc7b'
down_revision = '772194b1f5aa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('chats_settings', sa.Column('admin_id', postgresql.UUID(as_uuid=True),nullable=True))
    op.add_column('chats_settings', sa.Column('user_limit', sa.Integer ,default= 100))


def downgrade():
    op.drop_column('chats_settings', 'admin_id')
    op.drop_column('chats_settings', 'user_limit')
