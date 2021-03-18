"""Initial migration

Revision ID: 242ae2dca2a4
Revises: 
Create Date: 2021-03-18 14:38:47.144681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '242ae2dca2a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=60), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('commented_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['commented_user_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['addproduct.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
