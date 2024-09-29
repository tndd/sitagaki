from datetime import datetime
from os import getenv
from typing import List, Optional

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import Bar, BarSet
from alpaca.data.requests import Adjustment, StockBarsRequest
from alpaca.data.timeframe import TimeFrame

cli_hist = StockHistoricalDataClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)

"""
TODO: 機能分離 extract系統
    この場所はget系のみにしたい。
    extractのような処理というのはprocessディレクトリみたいなのを作って、
    そちらに配置するべきな気がする。

TODO: 機能分離 bar,quote,trade
    このままではbar,quote,tradeが同じディレクトリに配置されることとなり、
    混乱を招く可能性があるので注意。これは杞憂かもしれないが。
"""


def extract_bar_list_alpaca_api_from_barset(barset: BarSet) -> List[Bar]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))


def get_barset_alpaca_api(
        symbol: str,
        timeframe: TimeFrame,
        adjustment: Adjustment,
        start: datetime,
        end: Optional[datetime] = None,
        limit: Optional[int] = None
) -> BarSet:
    """
    日足のヒストリカルバー情報を取得。
    endを指定しなかった場合、可能な限り直近のデータを取得するようになってる。
    """
    rq = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        adjustment=adjustment,
        start=start,
        end=end if end else None,
        limit=limit
    )
    return cli_hist.get_stock_bars(rq)


def get_bar_alpaca_api_list(
        symbol: str,
        timeframe: TimeFrame,
        adjustment: Adjustment,
        start: datetime,
        end: Optional[datetime] = None,
        limit: Optional[int] = None
) -> List[Bar]:
    """
    日足のヒストリカルバー情報を取得。
    endを指定しなかった場合、可能な限り直近のデータを取得するようになってる。

    取得したBarSetはそのままリポジトリ側が扱うのは難しい。
    そこでこの関数ではBarSetからBarのリストを取り出して返却するまで行う。
    """
    barset = get_barset_alpaca_api(symbol, timeframe, adjustment, start, end, limit)
    return extract_bar_list_alpaca_api_from_barset(barset)