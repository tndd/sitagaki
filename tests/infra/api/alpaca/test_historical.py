from alpaca.data.models.bars import BarSet

from infra.api.alpaca.historical import Timeframe, get_bars


def test_get_bars():
    timeframe = Timeframe.Day
    bars = get_bars(
        symbol='AAPL',
        start='2023-01-01',
        timeframe=timeframe
    )
    assert isinstance(bars, BarSet)