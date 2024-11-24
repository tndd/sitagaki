from datetime import datetime

from fixture.infra.db.peewee.table.alpaca.bar import (
    factory_table_bar_alpaca_latest_timestamps,
)
from src.infra.adapter.origin.alpaca.bar.model import (
    arrive_symbol_timestamp_dict_from_table,
)


def test_basic():
    """
    存在しないシンボルについてはきちんとtimestamp=Noneで埋められてるかを確認
    """
    # AAPL,GOOGのtable
    tables = factory_table_bar_alpaca_latest_timestamps()
    # 存在しないXXXX,YYYYも指定
    symbol_timestamps = arrive_symbol_timestamp_dict_from_table(
        symbols=["ARQ", "BAL", "ALM", "XXXX", "YYYY"],
        tables=tables
    )
    # 存在しないXXXX,YYYYも含めて5件
    assert len(symbol_timestamps) == 5
    # ARQ,BAL,ALMの値はdatetime
    assert isinstance(symbol_timestamps['ARQ'], datetime)
    assert isinstance(symbol_timestamps['BAL'], datetime)
    assert isinstance(symbol_timestamps['ALM'], datetime)
    # XXXX,YYYYの値はNone。存在しないため。
    assert symbol_timestamps['XXXX'] is None
    assert symbol_timestamps['YYYY'] is None


def test_ommit_symbols():
    """
    symbolsの指定を省略した場合、
    変換が期待通り行われていることを確認
    """
    # AAPL,GOOGのtable
    tables = factory_table_bar_alpaca_latest_timestamps()
    # symbolsを省略
    symbol_timestamps = arrive_symbol_timestamp_dict_from_table(
        tables=tables
    )
    # ARQ,BAL,ALM3件分のデータ
    assert len(symbol_timestamps) == 3
    # その３件のデータは本当にARQ,BAL,ALMか？
    assert 'ARQ' in symbol_timestamps
    assert 'BAL' in symbol_timestamps
    assert 'ALM' in symbol_timestamps