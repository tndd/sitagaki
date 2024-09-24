from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar.arrive import (
    arrive_bar_list_from_alpaca_api,
    arrive_bar_list_from_peewee_table,
)
from infra.adapter.materia.bar.depart import (
    depart_bar_list_to_peewee_table,
    depart_timeframe_to_alpaca_api,
)
from infra.api.alpaca.historical import get_bars
from infra.db.peewee import PeeweeClient
from infra.db.stmt.materia.bar import get_stmt_select_bar


@dataclass
class BarRepository:
    cli_db: PeeweeClient

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
        bar_list_alpaca_api = get_bars(
            symbol=symbol,
            timeframe=depart_timeframe_to_alpaca_api(timeframe),
            start=start,
            end=end
        )
        # 変換: alpaca_api -> domain
        bar_list = arrive_bar_list_from_alpaca_api(bar_list_alpaca_api)
        # 変換: domain -> peewee_table
        bar_list_peewee_table = depart_bar_list_to_peewee_table(bar_list)
        # DBのモデルリストを保存
        self.cli_db.insert_models(bar_list_peewee_table)


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
        return arrive_bar_list_from_peewee_table(bars_sqlm)