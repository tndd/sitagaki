from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import (
    adapt_bar_list_sqlm_to_domain,
    adapt_timeframe_domain_to_alpaca,
)
from infra.api.alpaca.historical import get_bars
from infra.db.sqlmodel import SQLModelClient
from infra.db.stmt.materia.bar import get_stmt_select_bar
from infra.process.api.alpaca.historical import adapt_bar_alpaca_list_to_sqlm


@dataclass
class BarRepository:
    cli_db: SQLModelClient

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
            timeframe=adapt_timeframe_domain_to_alpaca(timeframe),
            start=start,
            end=end
        )
        # HACK: パフォーマンスのため、alpaca -> sqlmの変換をdomainを介さず直接行っている。
        tbl_bars = adapt_bar_alpaca_list_to_sqlm(bars_alpc, timeframe)
        # DBのモデルリストを保存
        self.cli_db.insert_models(tbl_bars)


    def fetch_bars_from_local(
            self,
            symbol: str,
            timeframe: Timeframe,
            start: datetime = datetime(2000, 1, 1),
            end: datetime = datetime.now()
    ) -> None:
        """
        ローカルのDBから指定されたシンボルのbarを取得する。

        デフォルトの取得範囲は2000-01-01~now。
        """
        # 取得に必要なstmtを作成
        stmt = get_stmt_select_bar(
            symbol=symbol,
            timeframe=timeframe,
            start=start,
            end=end
        )
        # barデータをDBから取得
        bars_sqlm = self.cli_db.select_models(stmt)
        # 取得物をドメイン層のbarモデルのリストに変換して返す
        return adapt_bar_list_sqlm_to_domain(bars_sqlm)