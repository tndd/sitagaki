from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca_latest_timestamps,
)
from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe
from src.domain.origin.alpaca.bar.model import SymbolTimestampSet
from src.domain.origin.alpaca.bar.repository import REPO_CHART


def test_basic():
    factory_table_bar_alpaca_latest_timestamps(INSERT=True)
    symbol_timestamp_set = REPO_CHART.fetch_latest_symbol_timestamp_set(
        timeframe=Timeframe.MIN,
        adjustment=Adjustment.RAW,
        symbols=["ARQ", "BAL", "ALM"]
    )
    assert isinstance(symbol_timestamp_set, SymbolTimestampSet)
    assert len(symbol_timestamp_set.data) == 3
