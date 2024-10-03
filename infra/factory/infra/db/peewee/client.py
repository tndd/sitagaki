from enum import Enum

from peewee import MySQLDatabase, SqliteDatabase
from pydantic import BaseModel

from infra.db.peewee.client import DB_PROXY, PeeweeClient


class DBMode(Enum):
    TEST = 'test'
    DEV = 'dev'
    PROD = 'prod'


class DBProfile(BaseModel):
    db_name: str
    port: int


def get_db_profile_mysql(mode: DBMode) -> DBProfile:
    if mode == DBMode.TEST:
        return DBProfile(
            db_name='fuli_test',
            port=6000,
        )
    elif mode == DBMode.DEV:
        return DBProfile(
            db_name='fuli_dev',
            port=6001,
        )
    elif mode == DBMode.PROD:
        return DBProfile(
            db_name='fuli_prod',
            port=6002,
        )
    else:
        raise ValueError(f'Invalid DBMode: {mode}')


def factory_peewee_client_mysql(mode: DBMode) -> PeeweeClient:
    db_profile = get_db_profile_mysql(mode)
    db = MySQLDatabase(
        db_name=db_profile.db_name,
        user='mysqluser',
        password='mysqlpassword',
        host='localhost',
        port=db_profile.port,
    )
    DB_PROXY.initialize(db)
    return PeeweeClient(db)


def factory_peewee_client_sqlite() -> PeeweeClient:
    test_db_sqlite = SqliteDatabase(':memory:')
    DB_PROXY.initialize(test_db_sqlite)
    return PeeweeClient(test_db_sqlite)
