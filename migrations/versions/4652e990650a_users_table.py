"""users table

Revision ID: 4652e990650a
Revises: 
Create Date: 2020-05-10 03:13:29.269470

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "4652e990650a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("stack_size", sa.Integer(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_name"), "user", ["name"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_name"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
