"""add content column to posts table

Revision ID: 61c106f6fed9
Revises: bc5e18fd749e
Create Date: 2024-12-10 16:42:49.308671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61c106f6fed9'
down_revision: Union[str, None] = 'bc5e18fd749e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
