from alpaca.data.models.bars import Bar as AlpcBar
from alpaca.data.timeframe import TimeFrame as AlpcTimeFrame

from domain.materia.bar.model import Bar, Timeframe


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


def adapt_to_sqlm_bar(bar: Bar) -> AlpcBar:
    # TODO: まずはDB側のBarテーブル定義が先
    pass