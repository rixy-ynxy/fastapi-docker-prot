"""create_second_tables

Revision ID: baa7d649a431
Revises: 12056735bd4e
Create Date: 2022-12-14 16:32:03.997362

"""

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic
revision = 'baa7d649a431'
down_revision = '12056735bd4e'
branch_labels = None
depends_on = None


def create_users_table() -> None:
  op.create_table(
    "users",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.Text, nullable=False, index=True),
    sa.Column("description", sa.Text, nullable=True),
    sa.Column("color_type", sa.Text, nullable=False),
    sa.Column("age", sa.Numeric(10, 1), nullable=False),
  )


def upgrade() -> None:
  create_users_table()


def downgrade() -> None:
  op.drop_table("users")
