from datetime import datetime

from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca_list_times_shuffle,
)
from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe
from src.domain.origin.alpaca.bar.model import SymbolTimestampSet
from src.domain.origin.alpaca.bar.repository import REPO_CHART


def test_basic():
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    symbol_timestamp_set = REPO_CHART.fetch_latest_symbol_timestamp_set(
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
    )
    assert isinstance(symbol_timestamp_set, SymbolTimestampSet)
    assert len(symbol_timestamp_set.data) == 2
    # 取得データはAAPL,GOOGであり、日付は最新であることを確認
    assert symbol_timestamp_set.data['AAPL'] == datetime(2020, 1, 5)
    assert symbol_timestamp_set.data['GOOG'] == datetime(2021, 1, 5)


def test_designate_symbols():
    """
    symbolsを指定した場合の動作

    存在するシンボルは無論の事、
    存在しないシンボルのtimeframeについてはNoneであることを確認。
    """
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    symbol_timestamp_set = REPO_CHART.fetch_latest_symbol_timestamp_set(
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        symbols=['AAPL', 'XXXX', 'YYYY']
    )
    assert isinstance(symbol_timestamp_set, SymbolTimestampSet)
    # 指定シンボル分の件数は取得される
    assert len(symbol_timestamp_set.data) == 3
    # AAPLについては最新の日付
    assert symbol_timestamp_set.data['AAPL'] == datetime(2020, 1, 5)
    # XXXX,YYYYについてはNone
    assert symbol_timestamp_set.data['XXXX'] is None
    assert symbol_timestamp_set.data['YYYY'] is None


def test_duplicate_symbol():
    """
    重複するシンボルを受け取ってしまった場合の動作

    # NOTE: 重複時の挙動
        SQLクエリは重複した条件を指定しても１回しかフィルタリングはしない。
        だからリポジトリ側で重複処理をしなかったとしても、重複による問題は起こらない。
    """
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    symbol_timestamp_set = REPO_CHART.fetch_latest_symbol_timestamp_set(
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        symbols=['AAPL', 'XXXX', 'YYYY', 'AAPL']
    )
    assert isinstance(symbol_timestamp_set, SymbolTimestampSet)
    # 指定シンボル分の件数は取得される
    assert len(symbol_timestamp_set.data) == 3
    # AAPLについては最新の日付
    assert symbol_timestamp_set.data['AAPL'] == datetime(2020, 1, 5)
    # XXXX,YYYYについてはNone
    assert symbol_timestamp_set.data['XXXX'] is None
    assert symbol_timestamp_set.data['YYYY'] is None