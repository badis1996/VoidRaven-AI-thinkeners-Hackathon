"""merge heads

Revision ID: 155727c9e3cd
Revises: 71f2f0eeee59, ae0529d68a8d
Create Date: 2025-02-16 15:54:52.317308

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "155727c9e3cd"
down_revision: Union[str, None] = ("71f2f0eeee59", "ae0529d68a8d")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
