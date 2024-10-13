from datetime import datetime, timedelta

import pytest
from alpaca.data.enums import Adjustment as AdjustmentAlpaca
from alpaca.data.models import Bar
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from src.infra.api.alpaca.bar import AlpacaApiBarClient

cli_alpaca = AlpacaApiBarClient()


def test_basic():
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
    assert all(bar.symbol == 'MOCKSYMBOL_30C779F3' for bar in bar_alpaca_api_list)


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
    'start',
    [
        datetime.now() + timedelta(seconds=1),
        datetime.now() + timedelta(minutes=15),
    ]
)
def test_invalid_start(start):
    """
    startが現在時刻や未来の日時を指定した場合エラーとなるかを検証
    """
    with pytest.raises(ValueError, match="EID:3e00e226"):
        cli_alpaca.get_bar_alpaca_api_list(
            symbol='AAPL',
            timeframe=TimeFrameAlpaca.Day,
            adjustment=AdjustmentAlpaca.RAW,
            start=start,
        )