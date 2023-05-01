"""added email column to 'users'

Revision ID: aacf8158fd63
Revises: 064c38c33acf
Create Date: 2023-05-01 16:59:16.739631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aacf8158fd63"
down_revision = "064c38c33acf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("email", sa.String(length=80), nullable=False))
        batch_op.create_unique_constraint("users_email_key", ["email"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("users_email_key", type_="unique")
        batch_op.drop_column("email")

    # ### end Alembic commands ###