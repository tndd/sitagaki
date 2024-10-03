from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.stock.chart.model import Timeframe
from infra.db.peewee.table.bar import TableBarAlpaca


def arrive_timeframe_from_peewee_table(bar_peewee_table: TableBarAlpaca) -> Timeframe:
    """
    PeeweeTable -> Timeframe
    """
    mapping = {
        1: Timeframe.MIN,
        2: Timeframe.HOUR,
        4: Timeframe.DAY,
        8: Timeframe.WEEK,
        16: Timeframe.MONTH,
    }
    return mapping[bar_peewee_table.timeframe]


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


def depart_timeframe_to_peewee_table(timeframe: Timeframe) -> int:
    """
    Timeframe:
        Domain -> PeeweeTable

    注意: TableBarAlpacaの定義を参照する事。
    """
    mapping = {
        Timeframe.MIN: 1,
        Timeframe.HOUR: 2,
        Timeframe.DAY: 4,
        Timeframe.WEEK: 8,
        Timeframe.MONTH: 16,
    }
    if timeframe not in mapping:
        raise ValueError(
            f"無効なTimeframe: {timeframe}。"
            f"サポートされているTimeframeは "
            f"{', '.join(map(str, mapping.keys()))} です。"
        )
    return mapping[timeframe]