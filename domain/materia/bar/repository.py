from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import (adapt_to_bar_list,
                                       adapt_to_tbl_bar_alpaca_list,
                                       adapt_to_timeframe_alpaca)
from infra.api.alpaca import get_bars
from infra.db.sqlmodel import SqlModelClient


@dataclass
class BarRepository:
    cli_db: SqlModelClient

    def pull_bars_from_online(
            self,
            symbol: str,
            timeframe: Timeframe,
            start: datetime = datetime(2000,1,1),
            end: Optional[datetime] = None
    ) -> None:
        """
        2000年からのbarデータをonlineから取得し、DBに保存する。
        データ取得開始時期(start)は指定可能。
        終了時期(end)省略時は可能な限り直近のデータを取得する。
        """
        # barsデータを取得
        bars_alpc = get_bars(
            symbol=symbol,
            timeframe=adapt_to_timeframe_alpaca(timeframe),
            start=start,
            end=end
        )
        # ドメイン層のbarモデルのリストに変換
        bars = adapt_to_bar_list(bars_alpc)
        # ドメイン層のモデルリストbarsをDBのモデルリストに変換
        tbl_bars = adapt_to_tbl_bar_alpaca_list(bars, timeframe)
        # DBのモデルリストを保存
        self.cli_db.insert_models(tbl_bars)


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