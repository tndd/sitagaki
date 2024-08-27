from os import getenv

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import BarSet
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as AlpcTimeFrame

cli = StockHistoricalDataClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)


def get_bars(
    symbol: str,
    timeframe: AlpcTimeFrame,
    start: str = '2000-01-01'
) -> BarSet:
    """
    日足のヒストリカルバー情報を取得。
    デフォルトの開始日は2000年元年とする。
    """
    rq = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start
    )
    return cli.get_stock_bars(rq)
