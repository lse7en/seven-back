"""empty message

Revision ID: 6c05718ff26c
Revises: 15ac1949356b
Create Date: 2024-11-10 13:58:41.929346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '6c05718ff26c'
down_revision: Union[str, None] = '15ac1949356b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rps_games',
    sa.Column('player1_id', sa.BigInteger(), nullable=False),
    sa.Column('player2_id', sa.BigInteger(), nullable=True),
    sa.Column('player1_choice', sa.Enum('ROCK', 'PAPER', 'SCISSORS', name='rpschoice'), nullable=True),
    sa.Column('player2_choice', sa.Enum('ROCK', 'PAPER', 'SCISSORS', name='rpschoice'), nullable=True),
    sa.Column('status', sa.Enum('WAITING_FOR_PLAYER', 'WAITING_FOR_CHOICES', 'COMPLETED', name='rpsgamestatus'), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['player1_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['player2_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rps_games_created_at'), 'rps_games', ['created_at'], unique=False)
    op.create_index(op.f('ix_rps_games_updated_at'), 'rps_games', ['updated_at'], unique=False)

    op.add_column('users', sa.Column('is_bot', sa.Boolean(), nullable=True))

    op.execute(
        """
        UPDATE users
        SET is_bot = false
        """
    )

    op.alter_column('users', 'is_bot', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
