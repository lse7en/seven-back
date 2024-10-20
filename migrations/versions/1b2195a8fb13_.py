"""empty message

Revision ID: 1b2195a8fb13
Revises: b9963871e2bc
Create Date: 2024-10-20 11:46:20.308535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '1b2195a8fb13'
down_revision: Union[str, None] = 'b9963871e2bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    task_status = sa.Enum('NOT_DONE', 'DONE', 'CLAIMED', name='taskstatus')
    task_status.create(op.get_bind())
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
