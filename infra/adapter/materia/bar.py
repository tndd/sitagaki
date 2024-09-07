from typing import List, Union

from alpaca.data.models import Bar as BarAlpaca
from alpaca.data.models import BarSet as BarSetAlpaca
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import (TblBarDayAlpaca, TblBarHourAlpaca,
                                TblBarMinAlpaca)


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


def adapt_bar_domain_to_sqlm(
    bar: Bar,
    timeframe: Timeframe
) -> Union[
    TblBarMinAlpaca,
    TblBarHourAlpaca,
    TblBarDayAlpaca
]:
    data = bar.model_dump()
    if timeframe is Timeframe.MIN:
        return TblBarMinAlpaca.model_validate(data)
    elif timeframe is Timeframe.HOUR:
        return TblBarHourAlpaca.model_validate(data)
    elif timeframe is Timeframe.DAY:
        return TblBarDayAlpaca.model_validate(data)
    pass


def adapt_bar_list_domain_to_sqlm_list(
        bars: List[Bar],
        timeframe: Timeframe
) -> List[Union[
    TblBarMinAlpaca,
    TblBarHourAlpaca,
    TblBarDayAlpaca
]]:
    return [adapt_bar_domain_to_sqlm(bar, timeframe) for bar in bars]



def adapt_barset_alpaca_to_bar_alpaca_list(barset: BarSetAlpaca) -> List[BarAlpaca]:
    return next(iter(barset.data.values()))