"""empty message

Revision ID: 7453f9d5e7c0
Revises: 5602979a9f94
Create Date: 2024-11-10 18:26:07.417689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.models.user import User
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision: str = '7453f9d5e7c0'
down_revision: Union[str, None] = '5602979a9f94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users = [
        User(id=-174265330, first_name="......", last_name=".....", is_bot=True),
        User(id=-57548023, first_name="Dorien", last_name="M", is_bot=True),
        User(id=-5780422828, first_name="∆MIR", last_name="None", is_bot=True),
        User(id=-467766077, first_name="Sajjad", last_name="None", is_bot=True),
        User(id=-181987481, first_name="Ali", last_name="Gh", is_bot=True),
        User(id=-172368231, first_name="Ali", last_name="None", is_bot=True),
        User(id=-6000331475, first_name="Seti", last_name="None", is_bot=True),
        User(id=-5994408989, first_name="M", last_name="None", is_bot=True),
        User(id=-1336396710, first_name="Sevda", last_name="None", is_bot=True),
        User(id=-5633370214, first_name="mahan amp", last_name="None", is_bot=True),
        User(id=-202220514, first_name="乙ﾑん乇Ð", last_name="None", is_bot=True),
        User(id=-5807560217, first_name="Sami", last_name="None", is_bot=True),
        User(id=-6872545988, first_name="Bonnie", last_name="James", is_bot=True),
        User(id=-6697472786, first_name="Ebenezer", last_name="Forson", is_bot=True),
        User(id=-742757231, first_name=".", last_name="None", is_bot=True),
        User(id=-6686281205, first_name="Abhi", last_name="Patil", is_bot=True),
        User(id=-342302454, first_name="Maral", last_name="None", is_bot=True),
        User(id=-528604631, first_name="Mhr∆D", last_name="None", is_bot=True),
        User(id=-70361661, first_name="Masoud", last_name="Shki", is_bot=True),
        User(id=-7008794419, first_name="ᵐᵃʰʲᵃᵈ", last_name="None", is_bot=True),
        User(id=-77065272, first_name="Mia", last_name="None", is_bot=True),
        User(id=-1698183117, first_name="ethipo", last_name="Cff", is_bot=True),
        User(id=-431185741, first_name="Shahyar", last_name="Tai", is_bot=True),
        User(id=-2076631928, first_name="Bhargav", last_name="Ram", is_bot=True),
        User(id=-443046401, first_name="Vito", last_name="None", is_bot=True),
        User(id=-385276964, first_name="Max", last_name="None", is_bot=True),
        User(id=-6892428416, first_name="No Name", last_name="None", is_bot=True),
        User(id=-6127624586, first_name="Eldar", last_name="İsmayilov", is_bot=True),
        User(id=-6617881188, first_name="Ibrohim", last_name="None", is_bot=True),
        User(id=-7281877284, first_name="isko", last_name="None", is_bot=True),
        User(id=-6450483571, first_name="Никита", last_name="None", is_bot=True),
        User(id=-7176808926, first_name="Виктория", last_name="None", is_bot=True),
        User(id=-6304543751, first_name="Josephine", last_name="Titilayo", is_bot=True),
        User(id=-6549282616, first_name="476744", last_name="None", is_bot=True),
        User(id=-6754005246, first_name="Артур", last_name="None", is_bot=True),
        User(id=-5713252637, first_name="Yusfmohamad", last_name="None", is_bot=True),
        User(id=-5242624109, first_name="Javohir", last_name="None", is_bot=True),
        User(id=-1123567084, first_name="Erа", last_name="None", is_bot=True),
        User(id=-6805052490, first_name="ALEXE", last_name="None", is_bot=True),
        User(id=-7148111549, first_name="И", last_name="М", is_bot=True),
    ]

    conn = op.get_bind()

    session = Session(bind=conn)


    session.add_all(users)
    session.commit()

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
