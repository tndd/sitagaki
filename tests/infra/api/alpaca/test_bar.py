from datetime import datetime, timedelta

import pytest
from alpaca.common.exceptions import APIError
from alpaca.data.models import Bar, BarSet
from alpaca.data.requests import Adjustment as AdjustmentAlpaca
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.api.alpaca.bar import (
    extract_bar_list_alpaca_api_from_barset,
    get_bar_alpaca_api_list,
    get_barset_alpaca_api,
)
from tests.utils.factory.infra.api.alpaca.bar import generate_barset_alpaca


### BarAlpaca ###
def test_mock_get_bar_alpaca_api_list(replace_with_mock_get_barset_alpaca_api):
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


def test_mock_get_bar_alpaca_api_list_empty_barset(replace_with_mock_get_barset_alpaca_api_fail_empty_barset):
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


### BarSetAlpaca ###
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
@pytest.mark.online_slow
@pytest.mark.parametrize("timeframe,adjustment", [
    (tf, adj) for tf in TIMEFRAMES for adj in ADJUSTMENTS
])
def test_get_barset_alpaca_api(timeframe, adjustment):
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
def test_get_barset_alpaca_api_not_exist_symbol():
    """
    [ONLINE]
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
def test_get_barset_alpaca_api_invalid_start_end():
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
def test_get_barset_alpaca_api_over_timestamp():
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


### Helper ###
def test_extract_bar_alpaca_list_api_from_barset():
    """
    BarSetの中からBarのリストを取り出す機能のテスト
    """
    # case1: 正常系
    barset_empty = generate_barset_alpaca()
    # BarSetの中からBarのリストを取り出す
    bars = extract_bar_list_alpaca_api_from_barset(barset_empty)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)

    """
    case2: BarSetが空の場合
        結果が十分に取得されている場合、
        空のBarSetが返されることは考えられる。

    期待結果:
        空のBarリストが返される。
    """
    # 空のBarSetを生成
    barset_empty = BarSet(raw_data={'NOSYMBOL': []})
    # BarSetの中からBarのリストを取り出す
    bars = extract_bar_list_alpaca_api_from_barset(barset_empty)
    assert isinstance(bars, list)
    assert len(bars) == 0