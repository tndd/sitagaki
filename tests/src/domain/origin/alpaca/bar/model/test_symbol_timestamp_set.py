from datetime import datetime, timedelta

from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe
from src.domain.origin.alpaca.bar.model import SymbolTimestampSet


def test_get_update_target_symbols():
    """
    更新対象のシンボルを抽出できているかを確認

    require未指定時、Noneと未来の日付のものが除外されていることを確認。
    """
    d = {
        'A': datetime(2000,1,1),
        'B': datetime(2001,1,1),
        'C': None,
        'D': datetime.now() + timedelta(days=1),
    }
    symbol_ts_set = SymbolTimestampSet(
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        data=d
    )
    symbols = symbol_ts_set.get_update_target_symbols()
    # 未来のDを除いた３件
    assert len(symbols) == 3
    assert 'A' in symbols
    assert 'B' in symbols
    assert 'C' in symbols


def test_get_update_target_symbols_cutoff():
    """
    cutoff指定時、それより前の日付はすべて対象となっているか
    """
    d = {
        'A': datetime(2000,1,1),
        'B': datetime(2001,1,1),
        'C': None,
        'D': datetime(2010,1,1),
        'E': datetime(2010,1,1,12,0,0)
    }
    symbol_ts_set = SymbolTimestampSet(
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        data=d
    )
    # 期限は2010-1-1の10時までを更新対象とする
    symbols = symbol_ts_set.get_update_target_symbols(
        cutoff=datetime(2010,1,1,10,0,0)
    )
    # 12時のEのみが対象外となる
    # datetime(2010,1,1) => datetime(2010,1,1,0,0,0)となるため
    assert len(symbols) == 4
    assert 'A' in symbols
    assert 'B' in symbols
    assert 'C' in symbols
    assert 'D' in symbols