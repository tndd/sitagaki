from datetime import datetime

from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca_list,
    factory_table_bar_alpaca_list_times_shuffle,
)
from src.infra.db.peewee.client import CLI_PEEWEE
from src.infra.db.peewee.query.origin.stock.chart import (
    get_query_select_latest_timestamp_of_bar_alpaca,
)
from src.infra.db.peewee.table.alpaca.bar import AdjustmentTable, TimeframeTable


def test_basic():
    factory_table_bar_alpaca_list(INSERT=True)
    query = get_query_select_latest_timestamp_of_bar_alpaca(
        symbols=['AAPL', 'GOOG'],
        timeframe=TimeframeTable.DAY,
        adjustment=AdjustmentTable.RAW,
    )
    result = CLI_PEEWEE.exec_query_fetch(query)
    # orderbyによりAAPL,GOOGの2件が返るはず
    assert len(result) == 2
    # AAPLの日付
    assert result[0].symbol == 'AAPL'
    assert result[0].timestamp == datetime(2020, 1, 3)
    # GOOGの日付
    assert result[1].symbol == 'GOOG'
    assert result[1].timestamp == datetime(2020, 1, 2)


def test_tables_shuffled():
    """
    シャッフルされたテーブルの一覧からも期待される最新の日付が取れるか確認
    """
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    query = get_query_select_latest_timestamp_of_bar_alpaca(
        symbols=['AAPL', 'GOOG'],
        timeframe=TimeframeTable.DAY,
        adjustment=AdjustmentTable.RAW,
    )
    result = CLI_PEEWEE.exec_query_fetch(query)
    # orderbyによりAAPL,GOOGの2件が返るはず
    assert len(result) == 2
    # AAPLの日付 (2020/1/5)
    assert result[0].symbol == 'AAPL'
    assert result[0].timestamp == datetime(2020, 1, 5)
    # GOOGの日付 (2021/1/5)
    assert result[1].symbol == 'GOOG'
    assert result[1].timestamp == datetime(2021, 1, 5)


def test_not_exist_symbol():
    """
    存在しないシンボルを指定した場合

    期待: 存在しないシンボルは無視されてリストが返る
    """
    factory_table_bar_alpaca_list(INSERT=True)
    # MSFTは存在しないシンボル
    query = get_query_select_latest_timestamp_of_bar_alpaca(
        symbols=['AAPL', 'GOOG', 'MSFT'],
        timeframe=TimeframeTable.DAY,
        adjustment=AdjustmentTable.RAW,
    )
    result = CLI_PEEWEE.exec_query_fetch(query)
    # MSFTは存在しないので、AAPL,GOOGの2件が返るはず
    assert len(result) == 2


def test_not_exist_symbol_all():
    """
    全部存在しないシンボルだった場合

    期待: 空のリスト
    """
    factory_table_bar_alpaca_list(INSERT=True)
    query = get_query_select_latest_timestamp_of_bar_alpaca(
        symbols=['MOCKSMB0', 'MOCKSMB1', 'MOCKSMB2'],
        timeframe=TimeframeTable.DAY,
        adjustment=AdjustmentTable.RAW,
    )
    result = CLI_PEEWEE.exec_query_fetch(query)
    assert len(result) == 0
