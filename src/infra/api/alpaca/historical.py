from os import getenv
from typing import List

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import Bar as AlpcBar
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
) -> List[AlpcBar]:
    """
    日足のヒストリカルバー情報を取得。
    デフォルトの開始日は2000年元年とする。
    """
    rq = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start
    )
    bars = cli.get_stock_bars(rq)
    # FIXME: このような変換メソッドはアダプタで行うべき？
    return bars.data[symbol]