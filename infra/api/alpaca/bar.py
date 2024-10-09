from dataclasses import dataclass
from datetime import datetime, timedelta

from alpaca.data.enums import Adjustment
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import Bar, BarSet
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from pydantic import BaseModel

from .client import DELAY, ROOT_START_DATETIME, historical_cli


class TimeRange(BaseModel):
    start: datetime
    end: datetime


@dataclass
class AlpacaApiBarClient:
    cli: StockHistoricalDataClient = historical_cli

    def get_barset_alpaca_api(
        self,
        symbol: str,
        timeframe: TimeFrame,
        adjustment: Adjustment,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int | None = None
    ) -> BarSet:
        time_range = get_safe_timerange(start, end)
        # リクエスト作成
        rq = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=timeframe,
            adjustment=adjustment,
            start=time_range.start,
            end=time_range.end,
            limit=limit
        )
        return self.cli.get_stock_bars(rq) # type: ignore

    def get_bar_alpaca_api_list(
        self,
        symbol: str,
        timeframe: TimeFrame,
        adjustment: Adjustment,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int | None = None
    ) -> list[Bar]:
        """
        日足のヒストリカルバー情報を取得。
        endを指定しなかった場合、可能な限り直近のデータを取得するようになってる。
            * 現在時刻から１５分前までのデータを取得できる。

        BarSetからBarのリストを取り出して返却するまで行う。
        """
        barset = self.get_barset_alpaca_api(symbol, timeframe, adjustment, start, end, limit)
        return extract_bar_list_alpaca_api_from_barset(barset)


### Helper ###
def extract_bar_list_alpaca_api_from_barset(barset: BarSet) -> list[Bar]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))


def get_safe_timerange(
    start: datetime | None,
    end: datetime | None
) -> TimeRange:
    """
    alpacaの時間指定のために、startとendを安全な形式にする。
    """
    end_safe = datetime.now() - timedelta(minutes=DELAY)
    # startに指定がない場合、ROOT_START_DATETIMEを指定
    if start is None:
        start = ROOT_START_DATETIME
    # endがNone or 今の時刻の15分前を超えていたらNoneにする
    if not end or end > end_safe:
        end = end_safe
    if start >= end:
        raise ValueError('startはendよりも新しい日付である必要があります。')
    print(start, end)
    return TimeRange(start=start, end=end)
