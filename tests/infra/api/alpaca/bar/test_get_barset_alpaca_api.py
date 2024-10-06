from datetime import datetime, timedelta

import pytest
from alpaca.common.exceptions import APIError
from alpaca.data.models import BarSet
from alpaca.data.requests import Adjustment as AdjustmentAlpaca
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.api.alpaca.bar import f, g, get_barset_alpaca_api


def test_mock_f(monkeypatch):
    assert 'original' == f()
    monkeypatch.setattr(
        'infra.api.alpaca.bar.f',
        lambda: 'mocked'
    )
    assert 'mocked' == f()


def test_mock_g(monkeypatch):
    assert 'original' == g()
    monkeypatch.setattr(
        'infra.api.alpaca.bar.f',
        lambda: 'mocked'
    )
    assert 'mocked' == g()



# 組み合わせのリスト作成
TIMEFRAMES = [
    TimeFrameAlpaca.Minute,
    TimeFrameAlpaca.Hour,
    TimeFrameAlpaca.Day,
    TimeFrameAlpaca.Week,
    TimeFrameAlpaca.Month
]
ADJUSTMENTS = [
    AdjustmentAlpaca.RAW,
    AdjustmentAlpaca.SPLIT,
    AdjustmentAlpaca.DIVIDEND,
    AdjustmentAlpaca.ALL
]
@pytest.mark.online
@pytest.mark.parametrize("timeframe,adjustment", [
    (tf, adj) for tf in TIMEFRAMES for adj in ADJUSTMENTS
])
def test_default(timeframe, adjustment):
    """
    BarSetを取得する機能の通信テスト
    TimeframeとAdjustmentの全ての組み合わせを試す。

    BarSetの中身からtimeframeとadjustmentを判定する術がないので、
    通信が正常に行えているかという観点でのテスト。
    """
    # timeframe X adjustmentの組み合わせを全通り試す
    barset = get_barset_alpaca_api(
        symbol="AAPL",
        start=datetime(2024,1,1),
        timeframe=timeframe,
        adjustment=adjustment,
        limit=5
    )
    # LATER: 将来的にはログなどの方法で中身を確認する方針に変更
    assert isinstance(barset, BarSet)
    # limitによる取得数制限の確認
    assert len(barset.data['AAPL']) == 5


@pytest.mark.online
def test_response_is_empty_barset():
    """
    存在しないシンボルを指定した場合の振る舞いテスト
    """
    SYMBOL_DUMMY = 'NOSYMBOL'
    barset_empty = get_barset_alpaca_api(
        symbol=SYMBOL_DUMMY,
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW
    )
    # barsetの中身 => {'data': {'NOSYMBOL': []}}
    assert isinstance(barset_empty, BarSet)
    assert len(barset_empty.data[SYMBOL_DUMMY]) == 0


@pytest.mark.online
def test_invalid_start_end():
    """
    startとendの指定が不適切な場合

    case1: start > end
        終了日より開始日の方が新しい場合

        期待値:
            * エラー発生(APIError)
            * エラーメッセージに'end should not be before start'が含まれる
    """
    with pytest.raises(Exception) as excinfo:
        barset = get_barset_alpaca_api(
            symbol='AAPL',
            start=datetime(2024,1,1),
            end=datetime(2023,1,1),
            timeframe=TimeFrameAlpaca.Day,
            adjustment=AdjustmentAlpaca.RAW
        )
    # エラータイプの確認
    assert excinfo.type == APIError
    assert 'end should not be before start' in str(excinfo.value)


@pytest.mark.online
def test_over_timestamp():
    """
    alpaca apiの制限を超えた日付を指定した場合のテスト
    get_barset_alpaca_api()の安全装置が機能しているかを確認。
    """
    barset = get_barset_alpaca_api(
        symbol='AAPL',
        start=datetime(2024,1,1),
        end=datetime.now() + timedelta(days=1), # endに未来の日付を指定
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW,
        limit=5
    )
    assert isinstance(barset, BarSet)
    assert len(barset.data['AAPL']) == 5
