from typing import List, Union

from alpaca.data.models import BarSet
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import (TblBarDayAlpaca, TblBarHourAlpaca,
                                TblBarMinAlpaca)


def adapt_to_timeframe_alpaca(timeframe: Timeframe) -> TimeFrameAlpaca:
    if timeframe is Timeframe.MIN:
        return TimeFrameAlpaca.Minute
    elif timeframe is Timeframe.HOUR:
        return TimeFrameAlpaca.Hour
    elif timeframe is Timeframe.DAY:
        return TimeFrameAlpaca.Day
    elif timeframe is Timeframe.WEEK:
        return TimeFrameAlpaca.Week
    elif timeframe is Timeframe.MONTH:
        return TimeFrameAlpaca.Month


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