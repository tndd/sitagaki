from fixture.operate import load_table_bar_alpaca_on_db
from src.domain.materia.stock.chart.const import Adjustment, Timeframe
from src.infra.db.peewee.query.materia.stock.chart import (
    get_query_select_latest_timestamp_of_bar_alpaca,
)


def test_basic():
    return # TODO: テストコードの作成
    load_table_bar_alpaca_on_db()

