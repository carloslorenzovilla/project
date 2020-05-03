"""empty message

Revision ID: ca3e07fcdd7c
Revises: 
Create Date: 2020-04-28 16:38:07.067536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca3e07fcdd7c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('profile_image', sa.String(
                        length=64), nullable=False),
                    sa.Column('email', sa.String(length=64), nullable=True),
                    sa.Column('username', sa.String(length=64), nullable=True),
                    sa.Column('password_hash', sa.String(
                        length=128), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'),
                    'users', ['username'], unique=True)
    op.create_table('zones',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_zones_name'), 'zones', ['name'], unique=False)
    op.create_table('locations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=True),
                    sa.Column('address', sa.String(length=64), nullable=True),
                    sa.Column('phone', sa.String(length=10), nullable=True),
                    sa.Column('website', sa.String(length=64), nullable=True),
                    sa.Column('zone_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['zone_id'], ['zones.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_locations_name'),
                    'locations', ['name'], unique=False)
    op.create_table('items',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=False),
                    sa.Column('style', sa.String(length=64), nullable=False),
                    sa.Column('abv', sa.String(length=4), nullable=False),
                    sa.Column('ibu', sa.String(length=3), nullable=True),
                    sa.Column('location_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['location_id'], ['locations.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_items_abv'), 'items', ['abv'], unique=False)
    op.create_index(op.f('ix_items_ibu'), 'items', ['ibu'], unique=False)
    op.create_index(op.f('ix_items_name'), 'items', ['name'], unique=False)
    op.create_index(op.f('ix_items_style'), 'items', ['style'], unique=False)
    op.create_table('recommendations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('item_id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('logs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('item_id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    op.drop_table('recommendations')
    op.drop_index(op.f('ix_items_style'), table_name='items')
    op.drop_index(op.f('ix_items_name'), table_name='items')
    op.drop_index(op.f('ix_items_ibu'), table_name='items')
    op.drop_index(op.f('ix_items_abv'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_locations_name'), table_name='locations')
    op.drop_table('locations')
    op.drop_index(op.f('ix_zones_name'), table_name='zones')
    op.drop_table('zones')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
