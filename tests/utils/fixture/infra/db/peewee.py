import pytest
from peewee import SqliteDatabase

from infra.db.peewee.client import DB_PROXY, PeeweeClient


@pytest.fixture
def test_peewee_cli():
    test_db = SqliteDatabase(':memory:')
    DB_PROXY.initialize(test_db)
    yield PeeweeClient(test_db)
    test_db.close()
