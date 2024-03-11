"""set contact table to only contain unique entries

Revision ID: 6ee7b62b66c8
Revises: da69db64e365
Create Date: 2024-03-11 04:37:19.519493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ee7b62b66c8'
down_revision = 'da69db64e365'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contacts', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['owner_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contacts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###