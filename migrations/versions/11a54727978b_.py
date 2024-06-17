"""empty message

Revision ID: 11a54727978b
Revises: cf9dc6e54eaa
Create Date: 2024-06-13 13:49:12.921979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11a54727978b'
down_revision = 'cf9dc6e54eaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###