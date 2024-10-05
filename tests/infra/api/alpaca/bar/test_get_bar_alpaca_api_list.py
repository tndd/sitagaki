from datetime import datetime

from alpaca.data.models import Bar
from alpaca.data.requests import Adjustment as AdjustmentAlpaca
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.api.alpaca.bar import get_bar_alpaca_api_list


def test_default():
    """
    通信部分をモックにした簡易テスト
    """
    bar_alpaca_api_list = get_bar_alpaca_api_list(
        symbol='AAPL',
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW
    )
    assert isinstance(bar_alpaca_api_list, list)
    assert all(isinstance(bar, Bar) for bar in bar_alpaca_api_list)


def test_response_is_empty_barset(patch_with_mock_get_barset_alpaca_api_fail_empty_barset):
    """
    存在しない条件を入力し、apiから空のBarSetが帰ってきた際の振る舞いのテスト
    """
    # Mock通信
    bar_alpaca_api_list = get_bar_alpaca_api_list(
        symbol='NOSYMBOL',
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW
    )
    assert isinstance(bar_alpaca_api_list, list)
    assert len(bar_alpaca_api_list) == 0