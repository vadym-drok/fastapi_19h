"""add new column

Revision ID: 3f8ee0ad22ff
Revises: 5803ac7931a2
Create Date: 2024-07-06 07:50:28.579121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f8ee0ad22ff'
down_revision: Union[str, None] = '5803ac7931a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column('posts', 'content')
