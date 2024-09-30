import pytest

from tests.utils.factory.infra.db.peewee.bar import generate_table_bar_alpaca_list


@pytest.fixture
def prepare_table_bar_alpaca_on_db(test_peewee_cli):
    """
    BarデータをDBに登録する。
    """
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    test_peewee_cli.insert_models(table_bar_alpaca_list)
    yield
    # 事後処理
