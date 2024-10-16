from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca,
    factory_table_bar_alpaca_latest_timestamps,
    factory_table_bar_alpaca_list,
    factory_table_bar_alpaca_list_times_shuffle,
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


def test_factory_table_bar_alpaca_list_times_shuffle():
    """
    factory_table_bar_alpaca_list_times_shuffle()で生成されるデータの
    日付がランダムにシャッフルされていることを確認
    """
    table_bar_alpaca_list = factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    assert len(table_bar_alpaca_list) == 10
    # データが投入されたことを確認
    assert len(TableBarAlpaca.select()) == 10


def test_factory_table_bar_alpaca_latest_timestamps():
    table_models = factory_table_bar_alpaca_latest_timestamps(INSERT=True)
    assert isinstance(table_models, list)
    assert all(isinstance(table_model, TableBarAlpaca) for table_model in table_models)
    # ファクトリのBar本数は10本
    result = TableBarAlpaca.select()
    assert len(result) == 3
    assert all(isinstance(table_model, TableBarAlpaca) for table_model in result)
    # 3つのテーブルモデルのシンボルが、AAPL、MSFT、GOOGであることを確認
    symbols = set(model.symbol for model in result)
    assert symbols == {"ARQ", "BAL", "ALM"}
