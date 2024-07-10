"""'welcomed' column added to User.

Revision ID: 84a4ca1e12c4
Revises: 2e6e72d85fe3
Create Date: 2024-07-10 22:47:09.341837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84a4ca1e12c4'
down_revision = '2e6e72d85fe3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('location_id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('location_id'),
    sa.UniqueConstraint('location_id')
    )
    op.create_table('friendship',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('friend_id', sa.String(length=36), nullable=False),
    sa.Column('status', sa.Enum('pending', 'accepted'), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['friend_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('hangout',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('location_id', sa.String(length=36), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['location.location_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('hangout_attendee',
    sa.Column('hangout_attendee_id', sa.String(length=36), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('status', sa.Enum('pending', 'accepted', 'rejected'), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['hangout.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('hangout_attendee_id'),
    sa.UniqueConstraint('hangout_attendee_id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('welcomed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('welcomed')

    op.drop_table('hangout_attendee')
    op.drop_table('hangout')
    op.drop_table('friendship')
    op.drop_table('location')
    # ### end Alembic commands ###
