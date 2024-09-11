from datetime import datetime
from typing import List

from sqlmodel import Field, SQLModel

"""
TODO: testsというディレクトリ名はやめるべき
    testsという名前は特別なものであるため、改名した方が良さそうだ。
    それにこのファイルはおそらく１箇所からしか参照されない。
    だったらtest_sqlmodelに直書きしてもいいんじゃないか？
"""


class SampleUser(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime
    name: str
    email: str
    credit: int


def generate_sample_users(n: int = 10) -> List[SampleUser]:
    users = []
    users.append(
        SampleUser(
            created_at=datetime(1980,12,1),
            name='nagisa',
            email='surenagi333@blmail.tri',
            credit=10000
        )
    )
    users.append(
        SampleUser(
            created_at=datetime(1981,6,12),
            name='kazusa',
            email='casperi666@blmail.tri',
            credit=95
        )
    )
    users.append(
        SampleUser(
            created_at=datetime(1992,3,15),
            name='alice',
            email='hero810@blmail.ml',
            credit=30
        )
    )
    users.append(
        SampleUser(
            created_at=datetime(2000,3,22),
            name='astar',
            email='pepe423@stmail.com',
            credit=15000
        )
    )
    users.append(
        SampleUser(
            created_at=datetime(2000,3,22),
            name='helta',
            email='helta81@stmail.com',
            credit=110
        )
    )
    users.append(
        SampleUser(
            created_at=datetime(2001,9,5),
            name='carol',
            email='carol@mymail.net',
            credit=350
        )
    )
    users.append(
        SampleUser(
            created_at=datetime(2010,12,31),
            name='david',
            email='david@mymail.org',
            credit=700
        )
    )
    return users