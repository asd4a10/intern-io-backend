"""rename categor to category in companies

Revision ID: 8a591b2eeb1b
Revises: cb185b31aebc
Create Date: 2024-09-25 23:23:42.308732

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a591b2eeb1b"
down_revision: Union[str, None] = "cb185b31aebc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column("companies", sa.Column("category", sa.String(), nullable=True))
    # op.drop_column("companies", "categor")
    op.alter_column("companies", "categor", new_column_name="category")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('companies', sa.Column('categor', sa.VARCHAR(), autoincrement=False, nullable=True))
    # op.drop_column('companies', 'category')
    op.alter_column("companies", "category", new_column_name="categor")
    # ### end Alembic commands ###
