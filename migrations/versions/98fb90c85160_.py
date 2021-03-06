"""empty message

Revision ID: 98fb90c85160
Revises: adc05ac5e709
Create Date: 2018-01-29 14:19:11.963270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98fb90c85160'
down_revision = 'adc05ac5e709'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('items_email_key', 'items', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('items_email_key', 'items', ['email'])
    # ### end Alembic commands ###
