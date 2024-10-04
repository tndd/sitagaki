import pytest
from peewee import MySQLDatabase, SqliteDatabase

from infra.db.peewee.client import DB_PROXY, PeeweeClient, create_peewee_client


@pytest.fixture
def test_peewee_cli():
    """
    test_peewee_cliの入口
    """
    cli: PeeweeClient = create_peewee_client()
    cli.truncate_tables('TRUNCATE_TEST_TABLES')
    yield cli


@pytest.fixture
def test_peewee_cli_mysql():
    test_db_mysql = MySQLDatabase(
        'fuli_test',
        user='mysqluser',
        password='mysqlpassword',
        host='localhost',
        port=6002,
    )
    DB_PROXY.initialize(test_db_mysql)
    yield PeeweeClient(test_db_mysql)
    test_db_mysql.close()
