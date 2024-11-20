from datetime import datetime

from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca_list_times_shuffle,
)
from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe
from src.domain.origin.alpaca.bar.usecase import USE_CHART
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_basic():
    """
    既存のテーブルの状態を読み取り、
    適切な更新条件が設定され、
    実際にデータベースに更新が行われることを確認する。

    話をシンプルにするため、AAPLのデータについてのみテストを行う。
    """
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    symbols = ['AAPL']
    USE_CHART.update(symbols, Timeframe.DAY, Adjustment.RAW)
    # 元々のファクトリによる10件 + モック分の10件の合計20件
    assert len(TableBarAlpaca.select()) == 20
    # ファクトリによるデータの最新タイムスタンプはAAPL=2020-01-05
    # \ よってモック側のデータの最も古い日付は2020-01-05となる。
    #
    # \ まず情報の取得が行われたかを確認するため、モックシンボルが存在するかを確認する。
    symbol_mock = 'MOCK_AAPL|TF=1Day|AD=raw|START=2020-01-05 00:00:00|LIMIT=NONE'
    mock_records = TableBarAlpaca.select().where(TableBarAlpaca.symbol == symbol_mock)
    assert mock_records.exists()
    # モックデータ分の10件が存在することを確認
    assert len(mock_records) == 10
    # 次にモックシンボルのデータの最も古い日付が2020-01-05であるかを確認する。
    oldest_record = mock_records.order_by(TableBarAlpaca.timestamp.asc()).first()
    assert oldest_record.timestamp == datetime(2020, 1, 5, 0, 0, 0)
    assert oldest_record.timestamp == datetime(2020, 1, 5)  # 0は省略しても大丈夫であることを念のため確認


def test_multi_symbols():
    """
    複数のシンボルについてテストを行う。
    複数指定をした場合でも、複数更新が行われているかを確認。
    """
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    symbols = ['AAPL', 'GOOG']
    USE_CHART.update(symbols, Timeframe.DAY, Adjustment.RAW)
    # 元々のファクトリによる10件 + モック分の10件 * 2シンボル分の合計30件
    assert len(TableBarAlpaca.select()) == 30
    # AAPLのモックデータが存在するかを確認
    symbol_mock_aapl = 'MOCK_AAPL|TF=1Day|AD=raw|START=2020-01-05 00:00:00|LIMIT=NONE'
    mock_records_aapl = TableBarAlpaca.select().where(TableBarAlpaca.symbol == symbol_mock_aapl)
    assert mock_records_aapl.exists()
    assert len(mock_records_aapl) == 10
    # 最古の日付が2020-01-05であることを確認
    oldest_record = mock_records_aapl.order_by(TableBarAlpaca.timestamp.asc()).first()
    assert oldest_record.timestamp == datetime(2020, 1, 5, 0, 0, 0)
    # GOOGのモックデータが存在するかを確認 (GOOGのモックデータは2021-01-05から)
    symbol_mock_goog = 'MOCK_GOOG|TF=1Day|AD=raw|START=2021-01-05 00:00:00|LIMIT=NONE'
    mock_records_goog = TableBarAlpaca.select().where(TableBarAlpaca.symbol == symbol_mock_goog)
    assert mock_records_goog.exists()
    assert len(mock_records_goog) == 10
    # 最古の日付が2021-01-05であることを確認 (AAPLとGOOGの最古の日付は異なる)
    oldest_record = mock_records_goog.order_by(TableBarAlpaca.timestamp.asc()).first()
    assert oldest_record.timestamp == datetime(2021, 1, 5, 0, 0, 0)
