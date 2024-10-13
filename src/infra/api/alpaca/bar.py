from dataclasses import dataclass
from datetime import datetime, timedelta

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
        start: datetime | None = None,
        limit: int | None = None
    ) -> BarSet:
        start = get_safe_start(start)
        # リクエスト作成
        rq = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=timeframe,
            adjustment=adjustment,
            start=start,
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

        TODO: end廃止によるendの扱いについて
            endについては後方互換のため引数としては受け取っているが、
            それがget_barset_alpaca_apiに渡されることはない。
            後にendを全廃予定。
        """
        barset = self.get_barset_alpaca_api(symbol, timeframe, adjustment, start, limit)
        return extract_bar_list_alpaca_api_from_barset(barset)


### Helper ###
def extract_bar_list_alpaca_api_from_barset(barset: BarSet) -> list[Bar]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))


def get_safe_start(start: datetime | None) -> datetime:
    """
    渡されたstartを安全な日付に変換する
    """
    if start is None:
        # 未指定の場合はROOT_START_DATETIMEを指定
        return ROOT_START_DATETIME
    elif start < ROOT_START_DATETIME:
        # デフォルトの開始日時より前の日付が指定されている場合はデフォルトの開始日時を指定
        return ROOT_START_DATETIME
    elif start > datetime.now():
        # 現在時刻より未来の日付が指定されている場合はエラー
        raise ValueError("入力されたStartが現在時刻よりも未来が指定されてる。 EID:3e00e226")
    return start
