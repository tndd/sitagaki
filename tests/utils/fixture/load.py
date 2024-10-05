import pytest

import infra.db.peewee.client as peewee_cli
from infra.db.peewee.table.bar import TableBarAlpaca
from tests.utils.generate.infra.db.peewee.bar import generate_table_bar_alpaca_list


@pytest.fixture
def load_table_bar_alpaca_on_db():
    """
    BarデータをDBに登録する。
    """
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    peewee_cli.insert_models(table_bar_alpaca_list)


### TEST
# TODO: テスト移設。ここでは実行されない
def test_load_table_bar_alpaca_on_db():
    """
    BarデータがDBに登録されることを確認する。
    """
    result = TableBarAlpaca.select()
    # ファクトリのBar本数は10本
    assert len(result) == 10