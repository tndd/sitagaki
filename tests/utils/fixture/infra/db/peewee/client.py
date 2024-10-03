import pytest
from peewee import MySQLDatabase, SqliteDatabase

from infra.db.peewee.client import DB_PROXY, PeeweeClient
from infra.factory.infra.db.peewee.client import (
    DBMode,
    factory_peewee_client_mysql,
    factory_peewee_client_sqlite,
)


@pytest.fixture
def test_peewee_cli(test_peewee_cli_sqlite):
    """
    test_peewee_cliの入口
    """
    yield test_peewee_cli_sqlite


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
    truncate_tables(test_db_mysql)
    yield PeeweeClient(test_db_mysql)
    test_db_mysql.close()


@pytest.fixture
def test_peewee_cli_sqlite():
    db = factory_sqlite_peewee_client()
    yield db
    db.close()


def truncate_tables(db):
    db.connect()
    # 各テーブルをクリア
    tables = db.get_tables()
    with db.atomic():
        for table in tables:
            db.execute_sql(f"TRUNCATE TABLE {table}")
    db.close()