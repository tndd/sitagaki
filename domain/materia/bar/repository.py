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
        指定されたシンボルのbarデータをonlineから取得し、DBに保存する。

        start,endを指定しなかった場合、
        2000-01-01から可能な限り最新のデータを取得する。
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


    def fetch_bars_from_local(
            self,
            symbol: str,
            start: datetime = datetime(2000, 1, 1),
            end: datetime = datetime.now()
    ) -> None:
        """
        ローカルのDBから指定されたシンボルのbarを取得する。

        デフォルトの取得範囲は2000-01-01~now。
        """
        # IMPL
        pass