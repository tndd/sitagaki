import pytest
from peewee import PostgresqlDatabase, SqliteDatabase

from infra.db.peewee.client import DB_PROXY, PeeweeClient


@pytest.fixture
def test_peewee_cli(test_peewee_cli_sqlite):
    """
    test_peewee_cliの入口
    """
    yield test_peewee_cli_sqlite


@pytest.fixture
def test_peewee_cli_psql():
    test_db_psql = PostgresqlDatabase(
        'fuli_test',
        user='postgres',
        password='postgres',
        host='localhost',
        port=6002,
    )
    DB_PROXY.initialize(test_db_psql)
    yield PeeweeClient(test_db_psql)
    test_db_psql.close()


@pytest.fixture
def test_peewee_cli_sqlite():
    test_db_sqlite = SqliteDatabase(':memory:')
    DB_PROXY.initialize(test_db_sqlite)
    yield PeeweeClient(test_db_sqlite)
    test_db_sqlite.close()
