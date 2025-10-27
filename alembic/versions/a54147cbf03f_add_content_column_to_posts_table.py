"""add content column to posts table

Revision ID: a54147cbf03f
Revises: 31f2c7c3ef49
Create Date: 2025-10-27 15:04:27.940636

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a54147cbf03f"
down_revision: Union[str, Sequence[str], None] = "31f2c7c3ef49"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
