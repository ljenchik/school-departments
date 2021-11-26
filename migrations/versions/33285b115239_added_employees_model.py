"""Added employees model

Revision ID: 33285b115239
Revises: 40a8d74d9d55
Create Date: 2021-11-17 23:10:43.996826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33285b115239'
down_revision = '40a8d74d9d55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('role', sa.String(length=100), nullable=True),
    sa.Column('date_of_birth', sa.DateTime(), nullable=True),
    sa.Column('salary', sa.Float(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee')
    # ### end Alembic commands ###