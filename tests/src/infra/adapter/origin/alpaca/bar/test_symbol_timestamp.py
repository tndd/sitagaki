from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca_latest_timestamps,
)
from src.infra.adapter.origin.alpaca.bar.symbol_timestamp import (
    arrive_symbol_timestamp_ls_from_table,
)


def test_basic():
    """
    存在しないシンボルについてはきちんとtimestamp=Noneで埋められてるかを確認
    """
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


def test_ommit_symbols():
    """
    symbolsの指定を省略した場合、
    変換が期待通り行われていることを確認
    """
    # AAPL,GOOGのtable
    tables = factory_table_bar_alpaca_latest_timestamps()
    # symbolsを省略
    symbol_timestamps = arrive_symbol_timestamp_ls_from_table(
        tables=tables
    )
    # ARQ,BAL,ALM3件分のデータ
    assert len(symbol_timestamps) == 3
    # その３件のデータは本当にARQ,BAL,ALMか？
    assert symbol_timestamps[0].symbol == "ARQ"
    assert symbol_timestamps[1].symbol == "BAL"
    assert symbol_timestamps[2].symbol == "ALM"