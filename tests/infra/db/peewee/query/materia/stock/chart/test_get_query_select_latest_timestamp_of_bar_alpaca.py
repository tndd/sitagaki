from domain.materia.stock.chart.model import Adjustment, Timeframe
from infra.db.peewee.query.materia.stock.chart import (
    get_query_select_latest_timestamp_of_bar_alpaca,
)


def test_default():
    # TODO: テスト完成
    query = get_query_select_latest_timestamp_of_bar_alpaca(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW
    )
