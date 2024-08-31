"""Employee created

Revision ID: cb6c85f3ab13
Revises: dcfdd5c56c63
Create Date: 2024-08-31 13:20:39.410253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'cb6c85f3ab13'
down_revision: Union[str, None] = 'dcfdd5c56c63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
