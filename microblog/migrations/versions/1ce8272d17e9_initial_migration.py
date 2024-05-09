"""Initial migration

Revision ID: 1ce8272d17e9
Revises: 
Create Date: 2024-05-09 14:30:46.317488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ce8272d17e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=True),
    sa.Column('suburb', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('meal', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_order_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_order_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_order_last_name'), ['last_name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_order_last_name'))
        batch_op.drop_index(batch_op.f('ix_order_first_name'))
        batch_op.drop_index(batch_op.f('ix_order_email'))

    op.drop_table('order')
    # ### end Alembic commands ###
