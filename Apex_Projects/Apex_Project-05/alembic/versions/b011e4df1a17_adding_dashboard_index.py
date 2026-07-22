"""Adding Dashboard Index

Revision ID: b011e4df1a17
Revises: 039c8053b985
Create Date: 2026-07-06 18:11:53.802205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b011e4df1a17'
down_revision: Union[str, Sequence[str], None] = '039c8053b985'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    


def downgrade() -> None:
    """Downgrade schema."""
    pass
