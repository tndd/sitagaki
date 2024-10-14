from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca,
    factory_table_bar_alpaca_list,
    load_table_bar_alpaca_on_db,
)
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_load_table_bar_alpaca_on_db():
    """
    テスト用関数load_table_bar_alpaca_on_db()の動作確認
    """
    load_table_bar_alpaca_on_db()
    result = TableBarAlpaca.select()
    # ファクトリのBar本数は10本
    assert len(result) == 10


def test_factory_table_bar_alpaca():
    table_bar_alpaca = factory_table_bar_alpaca()
    assert isinstance(table_bar_alpaca, TableBarAlpaca)


def test_factory_table_bar_alpaca_list():
    table_bar_alpaca_list = factory_table_bar_alpaca_list()
    assert isinstance(table_bar_alpaca_list, list)
    assert all(isinstance(table_bar_alpaca, TableBarAlpaca) for table_bar_alpaca in table_bar_alpaca_list)
