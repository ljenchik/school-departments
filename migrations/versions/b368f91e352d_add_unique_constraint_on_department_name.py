"""Add unique constraint on department name

Revision ID: b368f91e352d
Revises: 33285b115239
Create Date: 2021-11-22 21:55:01.662695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b368f91e352d'
down_revision = '33285b115239'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'department', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'department', type_='unique')
    # ### end Alembic commands ###
