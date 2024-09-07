from datetime import datetime
from os import getenv
from typing import Optional

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import BarSet
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

cli = StockHistoricalDataClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)


def get_bars(
    symbol: str,
    timeframe: TimeFrameAlpaca,
    start: datetime,
    end: Optional[datetime] = None
) -> BarSet:
    """
    日足のヒストリカルバー情報を取得。
    endを指定しなかった場合、可能な限り直近のデータを取得するようになってる。
    """
    rq = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start,
        end=end if end else None
    )
    return cli.get_stock_bars(rq)
