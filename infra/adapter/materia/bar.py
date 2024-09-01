from typing import List, Union

from alpaca.data.models import BarSet
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import (TblBarDayAlpaca, TblBarHourAlpaca,
                                TblBarMinAlpaca)


def adapt_to_timeframe_alpaca(timeframe: Timeframe) -> TimeFrameAlpaca:
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


def adapt_to_tbl_bar_alpaca(
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



def adapt_to_bar_list(barset: BarSet) -> List[Bar]:
    return next(iter(barset.data.values()))