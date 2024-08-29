from typing import List

from alpaca.data.models import BarSet
from alpaca.data.timeframe import TimeFrame as AlpcTimeFrame

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import (TblBarDayAlpaca, TblBarHourAlpaca,
                                TblBarMinAlpaca)


def adapt_to_alpc_timeframe(timeframe: Timeframe) -> AlpcTimeFrame:
    if timeframe is Timeframe.MINUTE:
        return AlpcTimeFrame.Minute
    elif timeframe is Timeframe.HOUR:
        return AlpcTimeFrame.Hour
    elif timeframe is Timeframe.DAY:
        return AlpcTimeFrame.Day
    elif timeframe is Timeframe.WEEK:
        return AlpcTimeFrame.Week
    elif timeframe is Timeframe.MONTH:
        return AlpcTimeFrame.Month


def adapt_to_tbl_bar_min(bar: Bar) -> TblBarMinAlpaca:
    # TODO: 実装
    pass


def adapt_to_bar_list(barset: BarSet) -> List[Bar]:
    return next(iter(barset.data.values()))