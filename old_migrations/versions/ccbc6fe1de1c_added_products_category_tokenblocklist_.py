"""added products, category, tokenblocklist tables

Revision ID: ccbc6fe1de1c
Revises: 379e1f753044
Create Date: 2024-02-09 06:06:54.690122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccbc6fe1de1c'
down_revision = '379e1f753044'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokenblocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokenblocklist')
    # ### end Alembic commands ###
