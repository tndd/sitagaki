import json

import pytest
from pydantic import BaseModel

from infra.api.alpaca.historical import Timeframe, get_bars


@pytest.mark.ext
def test_get_bars():
    timeframe = Timeframe.Day
    bars = get_bars(
        symbol='AAPL',
        start='2023-01-01',
        timeframe=timeframe
    )
    # NOTE: 将来的にはログなどの方法で中身を確認する方針に変更
    # 出力検証用
    # with open('tests/out/test_get_bars.json', 'w') as f:
    #     f.write(
    #         json.dumps(
    #             [bar.model_dump() for bar in bars],
    #             default=str,
    #             indent=2
    #         )
    #     )
    assert isinstance(bars, list)
    assert all(isinstance(bar, BaseModel) for bar in bars)