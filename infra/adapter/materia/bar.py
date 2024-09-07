from typing import List

from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import (
    TblBarBase,
    TblBarDayAlpaca,
    TblBarHourAlpaca,
    TblBarMinAlpaca,
)


def adapt_timeframe_domain_to_alpaca(timeframe: Timeframe) -> TimeFrameAlpaca:
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


def adapt_bar_domain_to_sqlm(bar: Bar, timeframe: Timeframe) -> TblBarBase:
    data = bar.model_dump()
    if timeframe is Timeframe.MIN:
        return TblBarMinAlpaca.model_validate(data)
    elif timeframe is Timeframe.HOUR:
        return TblBarHourAlpaca.model_validate(data)
    elif timeframe is Timeframe.DAY:
        return TblBarDayAlpaca.model_validate(data)
    pass


def adapt_bar_sqlm_to_domain(bar_sqlm: TblBarBase) -> Bar:
    return Bar.model_validate(bar_sqlm.model_dump())


def adapt_bar_list_domain_to_sqlm(
        bars: List[Bar],
        timeframe: Timeframe
) -> List[TblBarBase]:
    return [adapt_bar_domain_to_sqlm(bar, timeframe) for bar in bars]


def adapt_bar_list_sqlm_to_domain(bars_sqlm: List[TblBarBase]) -> List[Bar]:
    return [adapt_bar_sqlm_to_domain(bar) for bar in bars_sqlm]
