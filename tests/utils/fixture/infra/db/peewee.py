import pytest
from peewee import CharField, DatabaseProxy, Model, SqliteDatabase

from infra.db.peewee import db_proxy


@pytest.fixture
def test_peewee_db():
    test_db = SqliteDatabase(':memory:')
    db_proxy.initialize(test_db)
    yield test_db
    test_db.close()
