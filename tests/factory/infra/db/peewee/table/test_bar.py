from infra.db.peewee.table.bar import TableBarAlpaca
from tests.utils.factory.infra.db.peewee.bar import (
    generate_table_bar_alpaca,
    generate_table_bar_alpaca_list,
)


def test_generate_table_bar_alpaca():
    table_bar_alpaca = generate_table_bar_alpaca()
    assert isinstance(table_bar_alpaca, TableBarAlpaca)


def test_generate_table_bar_alpaca_list():
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    assert isinstance(table_bar_alpaca_list, list)
    assert all(isinstance(table_bar_alpaca, TableBarAlpaca) for table_bar_alpaca in table_bar_alpaca_list)
