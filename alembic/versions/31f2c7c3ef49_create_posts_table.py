"""create posts table

Revision ID: 31f2c7c3ef49
Revises:
Create Date: 2025-10-27 14:47:13.812425

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "31f2c7c3ef49"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        # sa.Column("content", sa.String(), nullable=False),
        # sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
        # sa.Column(
        #     "created_at",
        #     sa.TIMESTAMP(timezone=True),
        #     server_default=sa.text("now()"),
        #     nullable=False,
        # ),
        # sa.Column("owner_id", sa.Integer(), nullable=False),
        # sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
