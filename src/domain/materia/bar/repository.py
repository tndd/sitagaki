from dataclasses import dataclass
from datetime import datetime

from domain.materia.bar.model import Timeframe
from infra.adapter.historical import adapt_timeframe
from infra.api.alpaca.historical import get_bars
from infra.db.sqlmodel import SqlModelClient


@dataclass
class BarRepository:
    cli_db: SqlModelClient


    def pull_bars_from_online(
            symbol: str,
            timeframe: Timeframe,
            start: datetime,
            end: datetime
    ) -> None:
        """
        条件:
            シンボルと開始日、終日を指定。
        効果:
            対象期間のローソク足をオンライン上から取得し保存する。
        """
        # IMPL
        # barsデータを取得
        bars = get_bars(
            symbol=symbol,
            timeframe=adapt_timeframe(timeframe),
            start=start
        )
        # barsデータを保存
        pass


    def fetch_bars_from_local(symbol: str, start: datetime, end: datetime):
        """
        条件:
            シンボルと開始日、終日を指定。
        戻り値:
            DFもしくはエラー
        効果:
            対象期間のローソク足をDB上から取得し保存する。
        """
        # IMPL
        pass