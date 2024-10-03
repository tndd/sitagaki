import pytest
from peewee import MySQLDatabase, SqliteDatabase

from infra.db.peewee.client import PeeweeClient
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
    cli = factory_peewee_client_mysql(DBMode.TEST)
    cli.truncate_tables(db_mode=DBMode.TEST)
    yield cli
    cli.close()


@pytest.fixture
def test_peewee_cli_sqlite():
    cli = factory_peewee_client_sqlite()
    yield cli
    cli.close()
