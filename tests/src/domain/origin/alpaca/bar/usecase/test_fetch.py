from datetime import datetime

from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca_list_times_shuffle,
)
from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe
from src.domain.origin.alpaca.bar.usecase import USE_CHART
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_basic():
    """
    基本的なデータの取得動作のテスト。
    AAPL,GOOGのデータがそれぞれ5件ずつ取得できることを確認する。
    """
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    chart_aapl = USE_CHART.fetch(symbol='AAPL', timeframe=Timeframe.DAY, adjustment=Adjustment.RAW)
    assert len(chart_aapl.bars) == 5
    chart_goog = USE_CHART.fetch(symbol='GOOG', timeframe=Timeframe.DAY, adjustment=Adjustment.RAW)
    assert len(chart_goog.bars) == 5


def test_update_mode():
    """
    更新モードが機能していることを確認

    # TODO: alpaca sdkの実装を変更し、このテストを実行可能にする
        モックはsymbolに引数の情報を含めるという仕様となっているため、
        fetchの引数として渡されたsymbolと、更新処理としてテーブルに保存されるsymbolが異なってしまう。
        そのためシームレスに古いデータと新しいデータを統合して返すという処理ができない。
    """
    return
    factory_table_bar_alpaca_list_times_shuffle(INSERT=True)
    # 更新モードが有効なので、もともとのデータの最新の日付が、
    # \ fetchされたデータの最も古い日付と一致することを確認する。
    chart_aapl = USE_CHART.fetch(
        symbol='AAPL',
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        update_mode=True
    )
    assert len(chart_aapl.bars) == 15
