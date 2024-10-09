from domain.materia.stock.chart.const import Adjustment, Timeframe
from infra.db.peewee.query.materia.stock.chart import (
    get_query_select_latest_timestamp_of_bar_alpaca,
)


def test_default():
    # TODO: _load_table_bar_alpaca_on_db()の汎用化が終わり次第
    pass
