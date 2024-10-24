from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca_latest_timestamps,
)
from src.infra.adapter.origin.alpaca.bar.symbol_timestamp import (
    arrive_symbol_timestamp_ls_from_table,
)


def test_basic():
    # AAPL,GOOGのtable
    tables = factory_table_bar_alpaca_latest_timestamps()
    # 存在しないXXXX,YYYYも指定
    symbol_timestamps = arrive_symbol_timestamp_ls_from_table(
        symbols=["ARQ", "BAL", "ALM", "XXXX", "YYYY"],
        tables=tables
    )
    # 存在しないXXXX,YYYYも含めて5件
    assert len(symbol_timestamps) == 5
    # ARQ,BAL,ALMのtimestampが存在する
    assert symbol_timestamps[0].timestamp is not None
    assert symbol_timestamps[1].timestamp is not None
    assert symbol_timestamps[2].timestamp is not None
    # XXXX,YYYYのtimestampはNone
    assert symbol_timestamps[3].timestamp is None
    assert symbol_timestamps[4].timestamp is None
