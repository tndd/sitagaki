from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from alpaca.data.enums import Adjustment
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import Bar, BarSet
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from .client import ROOT_START_DATETIME, historical_cli


@dataclass
class AlpacaApiBarClient:
    cli: StockHistoricalDataClient = historical_cli

    def get_barset_alpaca_api(
        self,
        symbol: str,
        timeframe: TimeFrame,
        adjustment: Adjustment,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> BarSet:
        # TODO: 安全な日付指定機能を分離。テストをしやすくするためにも
        # startに指定がない場合、ROOT_START_DATETIMEを指定
        if start is None:
            start = ROOT_START_DATETIME
        # endが今の時刻の15分前を超えていたらNoneにする
        if end and end > datetime.now() - timedelta(minutes=15):
            end = None
        # リクエスト作成
        rq = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=timeframe,
            adjustment=adjustment,
            start=start,
            end=end,
            limit=limit
        )
        return self.cli.get_stock_bars(rq) # type: ignore

    def get_bar_alpaca_api_list(
        self,
        symbol: str,
        timeframe: TimeFrame,
        adjustment: Adjustment,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Bar]:
        """
        日足のヒストリカルバー情報を取得。
        endを指定しなかった場合、可能な限り直近のデータを取得するようになってる。
            * 現在時刻から１５分前までのデータを取得できる。

        BarSetからBarのリストを取り出して返却するまで行う。
        """
        barset = self.get_barset_alpaca_api(symbol, timeframe, adjustment, start, end, limit)
        return extract_bar_list_alpaca_api_from_barset(barset)


### Helper ###
def extract_bar_list_alpaca_api_from_barset(barset: BarSet) -> List[Bar]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))
