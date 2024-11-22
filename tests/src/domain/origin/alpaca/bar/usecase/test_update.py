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
    # 1回目の時と違い、0件ではなく10件データが存在する。
    assert len(mock_records) == 10


def test_multi_symbols():
    """
    複数のシンボルについてテストを行う。
    AAPL,GOOGという複数指定をした場合でも、複数更新が行われているかを確認。
    """
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    # この時点でのテーブル件数は10件
    assert len(TableBarAlpaca.select()) == 10
    # AAPLのモックデータに、今後取得予定の範囲のデータが存在しないことを確認
    # \ AAPLのモックデータの最新の日付は2020-01-05
    mock_records_aapl = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == 'AAPL',
        TableBarAlpaca.timestamp > datetime(2020, 1, 5)
    )
    assert len(mock_records_aapl) == 0
    # GOOGのモックデータに、今後取得予定の範囲のデータが存在しないことを確認
    # \ GOOGのモックデータの最新の日付は2021-01-05。
    # \ AAPLとGOOGのモックデータの最古の日付は異なっているので注意。
    mock_records_goog = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == 'GOOG',
        TableBarAlpaca.timestamp > datetime(2021, 1, 5)
    )
    assert len(mock_records_goog) == 0
    # AAPLとGOOGのデータを取得。
    # \ この時点でデータ件数は、
    # \ 元データ10件 + 2シンボル分のモックデータ10件*2 - 最新（最古）の重複2シンボル分の2件
    # \ 合計28件となることが期待される。
    USE_CHART.update( ['AAPL', 'GOOG'], Timeframe.DAY, Adjustment.RAW)
    assert len(TableBarAlpaca.select()) == 28
    # AAPLの取得データ確認
    # \ 2020-01-05(を含む)からのデータが10件存在することを確認
    mock_records_aapl = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == 'AAPL',
        TableBarAlpaca.timestamp >= datetime(2020, 1, 5)
    )
    assert len(mock_records_aapl) == 10
    # GOOGのモックデータ確認
    # \ 2021-01-05(を含む)からのデータが10件存在することを確認
    mock_records_goog = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == 'GOOG',
        TableBarAlpaca.timestamp >= datetime(2021, 1, 5)
    )
    assert len(mock_records_goog) == 10
