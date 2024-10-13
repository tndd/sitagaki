from datetime import datetime

from fixture.infra.db.peewee.table.alpaca.bar import load_table_bar_alpaca_on_db
from src.infra.db.peewee.client import CLI_PEEWEE
from src.infra.db.peewee.query.materia.stock.chart import (
    get_query_select_latest_timestamp_of_bar_alpaca,
)
from src.infra.db.peewee.table.alpaca.bar import AdjustmentTable, TimeframeTable


def test_basic():
    load_table_bar_alpaca_on_db()
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
