import pytest

from infra.db.peewee.client import create_peewee_client
from tests.utils.mock.infra.db.peewee.bar import generate_table_bar_alpaca_list


@pytest.fixture
def prepare_table_bar_alpaca_on_db():
    """
    BarデータをDBに登録する。
    """
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    peewee_cli = create_peewee_client()
    peewee_cli.insert_models(table_bar_alpaca_list)
    yield
    # 事後処理
