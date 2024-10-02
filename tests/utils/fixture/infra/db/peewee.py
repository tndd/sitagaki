import pytest
from peewee import MySQLDatabase, SqliteDatabase

from infra.db.peewee.client import DB_PROXY, PeeweeClient


@pytest.fixture
def test_peewee_cli(test_peewee_cli_mysql):
    """
    test_peewee_cliの入口
    """
    yield test_peewee_cli_mysql


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
    reset_database(test_db_mysql)
    yield PeeweeClient(test_db_mysql)
    test_db_mysql.close()


@pytest.fixture
def test_peewee_cli_sqlite():
    test_db_sqlite = SqliteDatabase(':memory:')
    DB_PROXY.initialize(test_db_sqlite)
    yield PeeweeClient(test_db_sqlite)
    test_db_sqlite.close()


def reset_database(db):
    db.connect()
    # 各テーブルをクリア
    tables = db.get_tables()
    with db.atomic():
        for table in tables:
            db.execute_sql(f"TRUNCATE TABLE {table}")
    db.close()