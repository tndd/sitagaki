from datetime import datetime, timedelta

import pytest
from alpaca.data.enums import Adjustment as AdjustmentAlpaca
from alpaca.data.models import BarSet
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from src.infra.api.alpaca.bar import ROOT_START_DATETIME, AlpacaApiBarClient

cli_alpaca = AlpacaApiBarClient()



@pytest.mark.online
def test_basic():
    """
    基本的な通信テスト。
    デフォルト引数による動作検証。
    """
    # timeframe X adjustmentの組み合わせを全通り試す
    barset = cli_alpaca.get_barset_alpaca_api(
        symbol="AAPL",
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW,
        limit=5
    )
    # LATER: 将来的にはログなどの方法で中身を確認する方針に変更
    assert isinstance(barset, BarSet)
    # limitによる取得数制限の確認
    assert len(barset.data['AAPL']) == 5


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
def test_combination_tf_adj(timeframe, adjustment):
    """
    BarSetを取得する機能の通信テスト
    TimeframeとAdjustmentの全ての組み合わせを試す。

    BarSetの中身からtimeframeとadjustmentを判定する術がないので、
    通信が正常に行えているかという観点でのテスト。
    """
    # timeframe X adjustmentの組み合わせを全通り試す
    barset = cli_alpaca.get_barset_alpaca_api(
        symbol="AAPL",
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
    barset_empty = cli_alpaca.get_barset_alpaca_api(
        symbol=SYMBOL_DUMMY,
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW
    )
    # barsetの中身 => {'data': {'NOSYMBOL': []}}
    assert isinstance(barset_empty, BarSet)
    # SYMBOL_DUMMYがキーに存在することを確認
    assert SYMBOL_DUMMY in barset_empty.data
    # データが空であることを確認
    assert len(barset_empty.data[SYMBOL_DUMMY]) == 0


def test_future_start():
    """
    startに未来を指定した場合エラーが発生する
    """
    with pytest.raises(ValueError, match="EID:3e00e226"):
        barset = cli_alpaca.get_barset_alpaca_api(
            symbol='AAPL',
            start=datetime.now() + timedelta(days=1),
            timeframe=TimeFrameAlpaca.Day,
            adjustment=AdjustmentAlpaca.RAW
        )


@pytest.mark.online
@pytest.mark.parametrize("start", [
    ROOT_START_DATETIME,
    datetime(2020,1,1),
    None
])
def test_valid_starts(start):
    """
    適正なstartが指定されている場合のテスト
        1. ROOT_START_DATETIME
        2. 2020-01-01
        3. Noneを指定
    """
    barset = cli_alpaca.get_barset_alpaca_api(
        symbol='AAPL',
        start=start,
        timeframe=TimeFrameAlpaca.Day,
        adjustment=AdjustmentAlpaca.RAW,
        limit=3
    )
    assert isinstance(barset, BarSet)
    assert len(barset.data['AAPL']) == 3
