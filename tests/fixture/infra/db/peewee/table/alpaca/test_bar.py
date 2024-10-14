from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca,
    factory_table_bar_alpaca_list,
)
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_factory_table_bar_alpaca():
    table_bar_alpaca = factory_table_bar_alpaca(INSERT=True)
    assert isinstance(table_bar_alpaca, TableBarAlpaca)
    result = TableBarAlpaca.select()
    assert len(result) == 1


def test_factory_table_bar_alpaca_list():
    table_bar_alpaca_list = factory_table_bar_alpaca_list(INSERT=True)
    assert isinstance(table_bar_alpaca_list, list)
    assert all(isinstance(table_bar_alpaca, TableBarAlpaca) for table_bar_alpaca in table_bar_alpaca_list)
    # ファクトリのBar本数は10本
    result = TableBarAlpaca.select()
    assert len(result) == 10
    assert all(isinstance(table_bar_alpaca, TableBarAlpaca) for table_bar_alpaca in result)