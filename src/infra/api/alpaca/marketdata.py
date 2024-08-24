from os import getenv

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import BarSet
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as AlpcTimeFrame


class Timeframe(AlpcTimeFrame):
    """
    alpacaのtimeframeモデルをラッピングしただけのクラス
    """
    pass


def create_stock_historical_data_client() -> StockHistoricalDataClient:
    return StockHistoricalDataClient(
        api_key=getenv('APCA_KEY'),
        secret_key=getenv('APCA_SECRET')
    )


def get_bars(
    symbol: str,
    timeframe: Timeframe,
    start: str = '2000-01-01'
) -> BarSet:
    """
    日足のヒストリカルバー情報を取得。
    デフォルトの開始日は2000年元年とする。
    """
    cli = create_stock_historical_data_client()
    rq = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start
    )
    bars = cli.get_stock_bars(rq)
    return bars