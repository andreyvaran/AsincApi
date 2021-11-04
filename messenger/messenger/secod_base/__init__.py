def start_cash_users(base):
    from messenger.messenger.secod_base.users_cvc import csv_from_db
    csv_from_db(base)

if __name__ == '__main__':
    start_cash_users('../../users.csv')







# from alembic import op
# import sqlalchemy as sa
# from sqlalchemy.dialects import postgresql
#
# # revision identifiers, used by Alembic.
# revision = '917ade0262f5'
# down_revision = ''
# branch_labels = None
# depends_on = None
#
#
# def upgrade():
#     op.add_column('chats_settings', sa.Column('admin_id', postgresql.UUID(),nullable=True))
#     op.add_column('chats_settings', sa.Column('user_limit', sa.Integer ,default= 100))
#
#
# def downgrade():
#     op.drop_column('chats_settings', 'admin_id')
#     op.drop_column('chats_settings', 'user_limit')