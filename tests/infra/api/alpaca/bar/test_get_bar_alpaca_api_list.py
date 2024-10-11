from datetime import datetime

import pytest
from alpaca.data.enums import Adjustment as AdjustmentAlpaca
from alpaca.data.models import Bar
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from src.infra.api.alpaca.bar import AlpacaApiBarClient

cli_alpaca = AlpacaApiBarClient()


def test_default():
    """
    通信部分をモックにした簡易テスト
    """
    bar_alpaca_api_list = cli_alpaca.get_bar_alpaca_api_list(
        symbol='AAPL',
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW
    )
    assert isinstance(bar_alpaca_api_list, list)
    assert all(isinstance(bar, Bar) for bar in bar_alpaca_api_list)
    # モック化されているかの確認も兼ねたテスト
    assert len(bar_alpaca_api_list) == 5
    assert all(bar.symbol == 'MOCKSYMBOL' for bar in bar_alpaca_api_list)

def test_response_is_empty_barset(fx_replace_api_alpaca_get_stock_bars_empty):
    """
    存在しない条件を入力し、apiから空のBarSetが帰ってきた際の振る舞いのテスト
    """
    bar_alpaca_api_list = cli_alpaca.get_bar_alpaca_api_list(
        symbol='NOSYMBOL',
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW
    )
    assert isinstance(bar_alpaca_api_list, list)
    assert len(bar_alpaca_api_list) == 0


@pytest.mark.parametrize(
    'start,end',
    [
        (datetime(2020, 1, 1), datetime(2000, 1, 1)),
        (datetime(2001, 1, 1), datetime(2001, 1, 1)),
    ]
)
def test_invalid_time_range(start, end):
    """
    startがendよりも新しい日付であった場合にエラーとなるかの検証。

    test_reverse_start_endでも検証しているが、
    念のため、外部から使われるこちらの使う側でも検証する。

    0. 逆転
    1. 同じ日付
    """
    with pytest.raises(ValueError):
        cli_alpaca.get_bar_alpaca_api_list(
            symbol='AAPL',
            timeframe=TimeFrameAlpaca.Day,
            adjustment=AdjustmentAlpaca.RAW,
            start=start,
            end=end,
        )