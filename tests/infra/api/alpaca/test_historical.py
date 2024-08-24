from pydantic import BaseModel

from infra.api.alpaca.historical import Timeframe, get_bars


def test_get_bars():
    timeframe = Timeframe.Day
    bars = get_bars(
        symbol='AAPL',
        start='2023-01-01',
        timeframe=timeframe
    )
    assert isinstance(bars, list)
    assert all(isinstance(bar, BaseModel) for bar in bars)