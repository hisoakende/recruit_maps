"""Update like model

Revision ID: 68926d46c076
Revises: e29d7456f5b8
Create Date: 2024-01-21 22:20:49.649753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68926d46c076'
down_revision: Union[str, None] = 'e29d7456f5b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('like_tag_fkey', 'like', type_='foreignkey')
    op.create_foreign_key(None, 'like', 'tag', ['tag'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'like', type_='foreignkey')
    op.create_foreign_key('like_tag_fkey', 'like', 'tag', ['tag'], ['id'])
    # ### end Alembic commands ###
