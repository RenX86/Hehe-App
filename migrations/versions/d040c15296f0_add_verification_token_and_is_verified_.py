"""Add verification_token and is_verified fields

Revision ID: d040c15296f0
Revises: b79180f7c2dd
Create Date: 2025-03-14 13:01:47.989366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd040c15296f0'
down_revision = 'b79180f7c2dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artists', schema=None) as batch_op:
        batch_op.drop_index('idx_artist_name')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verification_token', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True))
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=250),
               type_=sa.String(length=250),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['verification_token'])

    with op.batch_alter_table('works', schema=None) as batch_op:
        batch_op.alter_column('artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_index('idx_rating')
        batch_op.drop_index('idx_title_gist', postgresql_using='gist')
        batch_op.drop_index('idx_title_trgm', postgresql_using='gin')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('works', schema=None) as batch_op:
        batch_op.create_index('idx_title_trgm', ['title'], unique=False, postgresql_using='gin')
        batch_op.create_index('idx_title_gist', ['title'], unique=False, postgresql_using='gist')
        batch_op.create_index('idx_rating', ['rating'], unique=False)
        batch_op.alter_column('artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=250),
               existing_nullable=True)
        batch_op.drop_column('is_verified')
        batch_op.drop_column('verification_token')

    with op.batch_alter_table('artists', schema=None) as batch_op:
        batch_op.create_index('idx_artist_name', ['artist_name'], unique=False)

    # ### end Alembic commands ###
