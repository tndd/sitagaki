from typing import List

from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import TableBarAlpaca


def depart_timeframe_alpaca_api(timeframe: Timeframe) -> TimeFrameAlpaca:
    """
    Timeframe:
        Domain -> Alpaca API
    """
    timeframe_map = {
        Timeframe.MIN: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Minute),
        Timeframe.HOUR: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Hour),
        Timeframe.DAY: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Day),
        Timeframe.WEEK: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Week),
        Timeframe.MONTH: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Month)
    }
    if timeframe not in timeframe_map:
        raise ValueError(
            f"無効なTimeframe: {timeframe}。"
            f"サポートされているTimeframeは "
            f"{', '.join(map(str, timeframe_map.keys()))} です。"
        )
    return timeframe_map[timeframe]


def depart_bar_peewee_table(bar: Bar, timeframe: Timeframe) -> TableBarAlpaca:
    """
    Bar:
        Domain -> Peewee Table
    """
    # TODO: 実装
    pass


def depart_bar_list_peewee_table(
        bars: List[Bar],
        timeframe: Timeframe
) -> List[TableBarAlpaca]:
    """
    Bar<List>:
        Domain -> Peewee Table
    """
    return [depart_bar_peewee_table(bar, timeframe) for bar in bars]
