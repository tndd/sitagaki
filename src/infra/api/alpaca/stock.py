from os import getenv

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


def f():
    cli = StockHistoricalDataClient(
        api_key=getenv('APCA_KEY'),
        secret_key=getenv('APCA_SECRET')
    )
    rq = StockBarsRequest(
        symbol_or_symbols='AAPL',
        timeframe=TimeFrame.Day,
        start='2023-01-01'
    )
    bars = cli.get_stock_bars(rq)
    return bars