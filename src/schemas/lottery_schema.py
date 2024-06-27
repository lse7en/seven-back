

from typing import Optional
from src.core.schema import BaseModel
from datetime import datetime, date
from src.schemas.user_schemas import User
from pydantic import computed_field

def decimal_to_base6(decimal_num):
    base6 = ""
    num = decimal_num 
    while num > 0:
        base6 = str(num % 6 + 1) + base6
        num //= 6
    # pad with 1s
    base6 = "1" * (8 - len(base6)) + base6
    return base6


class Ticket(BaseModel):
    """
    DTO for Ticket model.

    It returned when accessing Ticket models from the API.
    """
    id: int
    ticket_number: int

    @property
    def ticket(self) -> str:
        return decimal_to_base6(self.ticket_number)

    @computed_field
    @property
    def first_part(self) -> str:
        string = self.ticket[:6]
        return ' '.join(list(string))
    

    @computed_field
    @property
    def last_part(self) -> str:
        return self.ticket[6:]



class Participant(BaseModel):
    """
    DTO for User model.

    It returned when accessing User models from the API.
    """

    user: User
    activate_tickets_count: int
    tickets: list[Ticket] = []



