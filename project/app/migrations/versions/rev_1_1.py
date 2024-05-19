from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'rev_1_1'
down_revision = 'rev_1'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user', sa.Column('email', sa.String(length=120), nullable=False))

def downgrade():
    op.drop_column('user', 'email')