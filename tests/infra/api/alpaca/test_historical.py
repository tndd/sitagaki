import pytest
from alpaca.data.models import BarSet
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.api.alpaca.historical import get_bars


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
