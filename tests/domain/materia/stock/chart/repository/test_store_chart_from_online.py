import pytest

from domain.materia.stock.chart.model import Adjustment, Timeframe
from infra.adapter.materia.stock.chart.adjustment import (
    arrive_adjustment_from_peewee_table,
)
from infra.adapter.materia.stock.chart.timeframe import (
    arrive_timeframe_from_peewee_table,
)
from infra.db.peewee.table.bar import TableBarAlpaca


@pytest.mark.parametrize("timeframe,adjustment", [
    (tf, adj) for tf in Timeframe for adj in Adjustment
])
def test_all_combinations(
        test_chart_repo_mocked_with_alpaca_api,
        timeframe,
        adjustment
):
    """
    TimeframeとAdjustmentすべての組み合わせによる情報取得テスト

    LATER: alpaca_apiの通信部分のモックの戻り値
        もう少し引数に応じて結果変わるように、実際の動作っぽい動きにしたい。
    """
    test_chart_repo_mocked_with_alpaca_api.store_chart_from_online(
        symbol="AAPL",
        timeframe=timeframe,
        adjustment=adjustment,
        limit=5
    )
    bar_table_list = TableBarAlpaca.select()
    assert len(bar_table_list) == 5
    assert all(
        isinstance(bar, TableBarAlpaca) and
        arrive_timeframe_from_peewee_table(bar) == timeframe and
        arrive_adjustment_from_peewee_table(bar) == adjustment
        for bar in bar_table_list
    )
