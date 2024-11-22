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
    # この時点でのテーブル件数は10件
    assert len(TableBarAlpaca.select()) == 10
    # ここでAAPLかつ2020-01-05（を含まない）より新しいデータの件数は0件であることを確認しておく。
    # \ 2020-01-05よりも新しいデータは、これから取得されることが期待されているからだ。
    mock_records = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == 'AAPL',
        TableBarAlpaca.timestamp > datetime(2020, 1, 5)
    )
    assert len(mock_records) == 0
    # データを取得。ただしモックデータの最新の日付と取得データの最古の日付は重複する。
    # \ つまり元々の件数10件 + モックの件数10件 から重複する1件を引いた19件が期待値となる。
    USE_CHART.update(['AAPL'], Timeframe.DAY, Adjustment.RAW)
    assert len(TableBarAlpaca.select()) == 19
    # ファクトリによるデータの最新タイムスタンプはAAPL=2020-01-05
    # \ つまりAAPLかつ2020-01-05（を含む）より新しいデータの件数は10件となっているはずだ。
    mock_records = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == 'AAPL',
        TableBarAlpaca.timestamp >= datetime(2020, 1, 5)
    )
    assert len(mock_records) == 10


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
