import pytest
from alpaca.data.models import Bar, BarSet
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.api.alpaca import extract_bar_alpaca_list_from_barset, get_bars
from tests.utils.factory.infra.api.alpaca import generate_barset


@pytest.mark.ext
def test_get_bars():
    timeframe = TimeFrameAlpaca.Day
    bars = get_bars(
        symbol='AAPL',
        start='2024-01-01',
        timeframe=timeframe
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
    assert isinstance(bars, BarSet)


def test_extract_bar_alpaca_list_from_barset():
    """
    BarSetの中からBarのリストを取り出すアダプタのテスト
    """
    barset = generate_barset()
    bars = extract_bar_alpaca_list_from_barset(barset)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)
