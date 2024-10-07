from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.stock.chart.model import Timeframe
from infra.db.peewee.table.alpaca.bar import TableBarAlpaca, TimeframeTable


def arrive_timeframe_from_table(bar_table: TableBarAlpaca) -> Timeframe:
    """
    PeeweeTable -> Timeframe
    """
    mapping = {
        TimeframeTable.MIN: Timeframe.MIN,
        TimeframeTable.HOUR: Timeframe.HOUR,
        TimeframeTable.DAY: Timeframe.DAY,
        TimeframeTable.WEEK: Timeframe.WEEK,
        TimeframeTable.MONTH: Timeframe.MONTH,
    }
    return mapping[bar_table.timeframe]


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


def depart_timeframe_to_table(timeframe: Timeframe) -> TimeframeTable:
    """
    Timeframe:
        Domain -> PeeweeTable

    注意: TableBarAlpacaの定義を参照する事。
    """
    mapping = {
        Timeframe.MIN: TimeframeTable.MIN,
        Timeframe.HOUR: TimeframeTable.HOUR,
        Timeframe.DAY: TimeframeTable.DAY,
        Timeframe.WEEK: TimeframeTable.WEEK,
        Timeframe.MONTH: TimeframeTable.MONTH,
    }
    if timeframe not in mapping:
        raise ValueError(
            f"無効なTimeframe: {timeframe}。"
            f"サポートされているTimeframeは "
            f"{', '.join(map(str, mapping.keys()))} です。"
        )
    return mapping[timeframe]