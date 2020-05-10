"""tables

Revision ID: c064605eed64
Revises: 4652e990650a
Create Date: 2020-05-10 03:47:48.930287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c064605eed64'
down_revision = '4652e990650a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_table_name'), 'table', ['name'], unique=True)
    op.add_column('user', sa.Column('table_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'table', ['table_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'table_id')
    op.drop_index(op.f('ix_table_name'), table_name='table')
    op.drop_table('table')
    # ### end Alembic commands ###