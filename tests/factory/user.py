from datetime import datetime
from typing import List

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime
    name: str
    email: str
    credit: int


def generate_sample_users(n: int = 10) -> List[User]:
    users = []
    users.append(
        User(
            created_at=datetime(1980,12,1),
            name='nagisa',
            email='surenagi333@blmail.tri',
            credit=10000
        )
    )
    users.append(
        User(
            created_at=datetime(1981,6,12),
            name='kazusa',
            email='casperi666@blmail.tri',
            credit=95
        )
    )
    users.append(
        User(
            created_at=datetime(1992,3,15),
            name='alice',
            email='hero810@blmail.ml',
            credit=30
        )
    )
    users.append(
        User(
            created_at=datetime(2000,3,22),
            name='astar',
            email='pepe423@stmail.com',
            credit=15000
        )
    )
    users.append(
        User(
            created_at=datetime(2000,3,22),
            name='helta',
            email='helta81@stmail.com',
            credit=110
        )
    )
    users.append(
        User(
            created_at=datetime(2001,9,5),
            name='carol',
            email='carol@mymail.net',
            credit=350
        )
    )
    users.append(
        User(
            created_at=datetime(2010,12,31),
            name='david',
            email='david@mymail.org',
            credit=700
        )
    )
    return users