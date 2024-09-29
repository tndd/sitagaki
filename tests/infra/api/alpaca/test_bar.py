from datetime import datetime

import pytest
from alpaca.data.models import Bar, BarSet
from alpaca.data.requests import Adjustment
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.api.alpaca.bar import (
    extract_bar_list_alpaca_api_from_barset,
    get_bar_alpaca_api_list,
    get_barset_alpaca_api,
)
from tests.utils.factory.infra.api.alpaca.bar import generate_barset_alpaca

"""
TODO: 範囲超過エラーのテスト
    alpaca apiの制約として、１日前のデータまでしか取れない。
    それを超えた場合に、どのような振る舞いをするかのテスト

TODO: 全パターン取得テストを実装するか検討
    この振る舞いはリポジトリ側でも行ってるから実装すると役被りする。
    だがapiの信頼性担保という意味ではやるべきかもしれない。
"""


def test_mock_get_bar_alpaca_api_list(mock_get_barset_alpaca_api):
    """
    通信部分をモックにした簡易テスト
    """
    bar_alpaca_api_list = get_bar_alpaca_api_list(
        symbol='AAPL',
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(bar_alpaca_api_list, list)
    assert all(isinstance(bar, Bar) for bar in bar_alpaca_api_list)


def test_mock_get_bar_alpaca_api_list_empty_barset(mock_get_barset_alpaca_api_empty):
    """
    存在しない条件を入力し、apiから空のBarSetが帰ってきた際の振る舞いのテスト
    """
    # Mock通信
    bar_alpaca_api_list = get_bar_alpaca_api_list(
        symbol='NOSYMBOL',
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(bar_alpaca_api_list, list)
    assert len(bar_alpaca_api_list) == 0


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


@pytest.mark.online
def test_get_barset_alpaca_api():
    """
    [ONLINE]
        BarSetを取得する機能の通信テスト
    """
    barset = get_barset_alpaca_api(
        symbol='AAPL',
        start=datetime(2024,1,1),
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW,
        limit=10
    )
    # LATER: 将来的にはログなどの方法で中身を確認する方針に変更
    assert isinstance(barset, BarSet)
    # limitによる取得数制限の確認
    assert len(barset.data['AAPL']) == 10


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
        adjustment=Adjustment.RAW
    )
    # barsetの中身 => {'data': {'NOSYMBOL': []}}
    assert isinstance(barset_empty, BarSet)
    assert len(barset_empty.data[SYMBOL_DUMMY]) == 0