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

def depart_timeframe_to_peewee_table(timeframe: Timeframe) -> int:
    """
    Timeframe:
        Domain -> PeeweeTable

    注意: TableBarAlpacaの定義を参照する事。
    """
    timeframe_map = {
        Timeframe.MIN: 1,
        Timeframe.HOUR: 2,
        Timeframe.DAY: 4,
        Timeframe.WEEK: 8,
        Timeframe.MONTH: 16,
    }
    if timeframe not in timeframe_map:
        raise ValueError(
            f"無効なTimeframe: {timeframe}。"
            f"サポートされているTimeframeは "
            f"{', '.join(map(str, timeframe_map.keys()))} です。"
        )
    return timeframe_map[timeframe]


def depart_adjustment_to_peewee_table(adjustment: Adjustment) -> int:
    """
    Adjustment:
        Domain -> PeeweeTable

    注意: TableBarAlpacaの定義を参照する事。
    """
    adjustment_map = {
        Adjustment.RAW: 1,
        Adjustment.SPLIT: 2,
        Adjustment.DEVIDED: 4,
        Adjustment.ALL: 8,
    }
    if adjustment not in adjustment_map:
        raise ValueError(
            f"無効なAdjustment: {adjustment}。"
            f"サポートされているAdjustmentは "
            f"{', '.join(map(str, adjustment_map.keys()))} です。"
        )
    return adjustment_map[adjustment]


def depart_bar_to_peewee_table(
        bar: Bar,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment
) -> TableBarAlpaca:
    """
    Bar:
        Domain -> PeeweeTable

    これは基本的に外部からは使われることはない。
    """
    return TableBarAlpaca(
        symbol=symbol,
        timestamp=bar.timestamp,
        timeframe=depart_timeframe_to_peewee_table(timeframe),
        adjustment=depart_adjustment_to_peewee_table(adjustment),
        open=bar.open,
        high=bar.high,
        low=bar.low,
        close=bar.close,
        volume=bar.volume,
        vwap=bar.vwap,
    )


def depart_chart_to_peewee_table_list(chart: Chart) -> List[TableBarAlpaca]:
    """
    Chart -> PeeweeTable<List>
    """
    return [
        depart_bar_to_peewee_table(bar, chart.symbol, chart.timeframe, chart.adjustment)
        for bar in chart.bars
    ]
