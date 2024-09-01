from datetime import datetime
from os import getenv

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
    start: datetime
) -> BarSet:
    """
    日足のヒストリカルバー情報を取得。

    注意:
        この関数はデフォルトでは終わりの時期を指定しない。
        endを指定しなかった場合、sdk側の設計により可能な限り直近のデータを取得するから。
        そしてonline上からendの時期を指定したいという需要が今の所思い当たらない。

        それとあまりに直近のデータを指定できずnow()を使えないという問題もある。
    """
    rq = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start
    )
    return cli.get_stock_bars(rq)
