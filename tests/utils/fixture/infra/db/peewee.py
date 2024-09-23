import pytest
from peewee import SqliteDatabase

from infra.db.peewee import DB_PROXY


@pytest.fixture
def test_peewee_db():
    test_db = SqliteDatabase(':memory:')
    DB_PROXY.initialize(test_db)
    yield test_db
    test_db.close()
