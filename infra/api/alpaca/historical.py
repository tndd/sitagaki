from datetime import datetime
from os import getenv
from typing import List, Optional

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import Bar, BarSet
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from infra.adapter.materia.bar.process import extract_bar_list_alpaca_api_from_barset

cli_hist = StockHistoricalDataClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)


def extract_bar_list_alpaca_api_from_barset(barset: BarSet) -> List[Bar]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))


def get_bars(
        symbol: str,
        timeframe: TimeFrameAlpaca,
        start: datetime,
        end: Optional[datetime] = None
) -> List[Bar]:
    """
    日足のヒストリカルバー情報を取得。
    endを指定しなかった場合、可能な限り直近のデータを取得するようになってる。

    取得したBarSetはそのままリポジトリ側が扱うのは難しい。
    そこでこの関数ではBarSetからBarのリストを取り出して返却するまで行う。
    """
    barset = get_barset(symbol, timeframe, start, end)
    return extract_bar_list_alpaca_api_from_barset(barset)


def get_barset(
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
    return cli_hist.get_stock_bars(rq)
