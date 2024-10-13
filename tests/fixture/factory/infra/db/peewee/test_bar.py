from fixture.infra.db.peewee.table.alpaca.bar import (
    generate_table_bar_alpaca,
    generate_table_bar_alpaca_list,
)
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_generate_table_bar_alpaca():
    table_bar_alpaca = generate_table_bar_alpaca()
    assert isinstance(table_bar_alpaca, TableBarAlpaca)


def test_generate_table_bar_alpaca_list():
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    assert isinstance(table_bar_alpaca_list, list)
    assert all(isinstance(table_bar_alpaca, TableBarAlpaca) for table_bar_alpaca in table_bar_alpaca_list)
