from datetime import datetime

from sqlmodel import between, select
from sqlmodel.sql.expression import SelectOfScalar

from domain.materia.bar.model import Timeframe
from infra.db.table.bar import (TblBarDayAlpaca, TblBarHourAlpaca,
                                TblBarMinAlpaca)


def select_bar(
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime
) -> SelectOfScalar:
    """
    指定されたtimeframeの
    特定のシンボルのstart~endの間のbarデータを取得する。
    """
    bar_model = None
    if timeframe == Timeframe.MIN:
        bar_model = TblBarMinAlpaca
    elif timeframe == Timeframe.HOUR:
        bar_model = TblBarHourAlpaca
    elif timeframe == Timeframe.DAY:
        bar_model = TblBarDayAlpaca
    else:
        raise ValueError(f"Invalid timeframe: {timeframe}")
    stmt = select(bar_model) \
        .where(bar_model.symbol == symbol) \
        .where(between(bar_model.timestamp, start, end))
    return stmt