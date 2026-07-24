"""Initial migration

Revision ID: 13f937b1e38e
Revises: 3f93367af792
Create Date: 2026-07-03 22:41:16.651456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13f937b1e38e'
down_revision: Union[str, Sequence[str], None] = '3f93367af792'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
