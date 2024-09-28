import pytest
from alpaca.data.enums import Adjustment
from alpaca.data.models import Bar, BarSet
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.api.alpaca.historical import (
    extract_bar_list_alpaca_api_from_barset,
    get_bar_alpaca_api_list,
    get_barset_alpaca_api,
)
from tests.utils.factory.infra.api.alpaca import generate_barset_alpaca


def test_extract_bar_alpaca_list_api_from_barset():
    """
    BarSetの中からBarのリストを取り出す機能のテスト
    """
    # case1: 正常系
    barset_empty = generate_barset_alpaca()
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
    bars = extract_bar_list_alpaca_api_from_barset(barset_empty)
    assert isinstance(bars, list)
    assert len(bars) == 0


@pytest.mark.online
def test_get_barset_alpaca_api():
    """
    case1: 正常系
    """
    barset_empty = get_barset_alpaca_api(
        symbol='AAPL',
        start='2024-01-01',
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW
    )
    # LATER: 将来的にはログなどの方法で中身を確認する方針に変更
    assert isinstance(barset_empty, BarSet)
    print(barset_empty)

    """
    case2: 存在しないシンボル

    期待結果:
        結果が取得できずともBarSetが返される
    """
    SYMBOL_DUMMY = 'NOSYMBOL'
    barset_empty = get_barset_alpaca_api(
        symbol=SYMBOL_DUMMY,
        start='2024-01-01',
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW
    )
    # barsetの中身 => {'data': {'NOSYMBOL': []}}
    assert isinstance(barset_empty, BarSet)
    assert len(barset_empty.data[SYMBOL_DUMMY]) == 0



@pytest.mark.online
def test_get_bar_alpaca_api_list():
    """
    TODO: Mockを使った通信をシミュレートする
        test_get_barですでに通信は行われているので、ここでは通信部はモックにする。
        monkeypatchを使ってモックを作る。
    """
    """
    case1: 正常系
    """
    bar_alpaca_api_list = get_bar_alpaca_api_list(
        symbol='AAPL',
        start='2024-01-01',
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(bar_alpaca_api_list, list)
    assert all(isinstance(bar, Bar) for bar in bar_alpaca_api_list)

    """
    case2: 異常系
        存在しないシンボル

    期待結果:
        空のリストが返される
    """
    bar_alpaca_api_list = get_bar_alpaca_api_list(
        symbol='NOSYMBOL',
        start='2024-01-01',
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(bar_alpaca_api_list, list)
    assert len(bar_alpaca_api_list) == 0
