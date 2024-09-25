import pytest
from alpaca.data.enums import Adjustment
from alpaca.data.models import Bar, BarSet
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.api.alpaca.historical import (
    extract_bar_list_alpaca_api_from_barset,
    get_barset,
)
from tests.utils.factory.infra.api.alpaca import generate_barset_alpaca


@pytest.mark.online
def test_get_bars():
    """
    MEMO: barsの総合テストは冗長か？
        get_barsの動作はかなりget_barsetと被ってるから、
        barsetのテストを省略するべきだろうか？

        外部で使われるget_barsだけでいいだろう。
        test_get_barsetやtest_extract_bar_alpaca_list_from_barsetは
        その部品でしかないのだから、その品質はこの総合テストで担保されるべきもの。

        仮に外部との通信というコストを度外視できるなら、
        全関数についてテストを行いカバレッジ１００％を目指すべきだろう。
        そして外部との通信があるとはいえ負荷は最小限。
        それならこのテストを追加するくらい問題ないんじゃないか？
        こういう議論は通信容量が大容量で問題が実際に起こり始めた段階で行うべきではないか。
    """
    barset = get_barset(
        symbol='AAPL',
        start='2024-01-01',
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW
    )
    bars = extract_bar_list_alpaca_api_from_barset(barset)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)


@pytest.mark.online
def test_get_barset():
    barset = get_barset(
        symbol='AAPL',
        start='2024-01-01',
        timeframe=TimeFrameAlpaca.Day,
        adjustment=Adjustment.RAW
    )
    # NOTE: 将来的にはログなどの方法で中身を確認する方針に変更
    # 出力検証用
    # import json
    # with open('tests/out/test_get_bars.json', 'w') as f:
    #     f.write(
    #         json.dumps(
    #             bars.model_dump(),
    #             default=str,
    #             indent=2
    #         )
    #     )
    assert isinstance(barset, BarSet)


def test_extract_bar_alpaca_list_api_from_barset():
    """
    BarSetの中からBarのリストを取り出す機能のテスト
    """
    barset = generate_barset_alpaca()
    bars = extract_bar_list_alpaca_api_from_barset(barset)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)
