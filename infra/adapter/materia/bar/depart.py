from typing import List

from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.bar.model import Adjustment, Bar, Chart, Timeframe
from infra.db.table.bar import TableBarAlpaca


def depart_timeframe_to_alpaca_api(timeframe: Timeframe) -> TimeFrameAlpaca:
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


def depart_bar_to_peewee_table(
        bar: Bar,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment
) -> TableBarAlpaca:
    """
    Bar:
        Domain -> Peewee Table

    これは基本的に外部からは使われることはない。
    """
    # TODO: 実装
    pass


def depart_chart_to_peewee_table_list(chart: Chart) -> List[TableBarAlpaca]:
    """
    Chart -> Peewee Table<List>
    """
    return [
        depart_bar_to_peewee_table(bar, chart.symbol, chart.timeframe, chart.adjustment)
        for bar in chart.bars
    ]
