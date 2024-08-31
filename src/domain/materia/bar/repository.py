from dataclasses import dataclass
from datetime import datetime

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import (adapt_to_bar_list,
                                       adapt_to_timeframe_alpaca)
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
        # barsデータを取得
        bars_alpc = get_bars(
            symbol=symbol,
            timeframe=adapt_to_timeframe_alpaca(timeframe),
            start=start
        )
        # ドメイン層のbarモデルのリストに変換
        bars = adapt_to_bar_list(bars_alpc)
        # TODO: barsデータを保存
        """
            1. barsをdbのモデルのリストに変換
            2. dbモデルリストを保存
        """
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