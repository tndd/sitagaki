from os import getenv
from typing import List

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as AlpcTimeFrame
from pydantic import BaseModel


class Timeframe(AlpcTimeFrame):
    """
    alpacaのtimeframeモデルをラッピングしただけのクラス

    指定できる形式
    - Minute
    - Hour
    - Day
    - Week
    - Month
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
) -> List[BaseModel]:
    """
    日足のヒストリカルバー情報を取得。
    デフォルトの開始日は2000年元年とする。

    戻り値について:
        * 条件に合致するBar(BaseModel)のリスト
        * Barを構成する情報
            - symbol (str): バーを形成するのティッカー識別子。
            - timestamp (datetime): バーの終了タイムスタンプ。
            - open (float): 期間の開始価格。
            - high (float): 期間中の高値。
            - low (float): 期間中の安値。
            - close (float): 期間の終値。
            - volume (float): 期間で取引されたボリューム。
            - trade_count (Optional[float]): 発生した取引数。
            - vwap (Optional[float]): ボリューム加重平均価格。
            - exchange (Optional[float]): バーが形成された取引所。
    """
    cli = create_stock_historical_data_client()
    rq = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start
    )
    bars = cli.get_stock_bars(rq)
    return list(bars.data.values())[0]