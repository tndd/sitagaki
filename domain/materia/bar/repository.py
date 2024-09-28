from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.materia.bar.adapter import (
    arrive_chart_from_bar_alpaca_api_list,
    arrive_chart_from_peewee_table,
    depart_adjustment_to_alpaca_api,
    depart_chart_to_peewee_table_list,
    depart_timeframe_to_alpaca_api,
)
from domain.materia.bar.model import Adjustment, Timeframe
from infra.api.alpaca.historical import get_bar_alpaca_api_list
from infra.db.peewee.client import PeeweeClient
from infra.db.peewee.query.materia.bar import get_query_select_bar_alpaca


@dataclass
class BarRepository:
    cli_db: PeeweeClient

    def pull_chart_from_online(
            self,
            symbol: str,
            timeframe: Timeframe,
            adjustment: Adjustment,
            start: datetime = datetime(2000,1,1),
            end: Optional[datetime] = None
    ) -> None:
        """
        指定されたシンボルのbarデータをonlineから取得し、DBに保存する。

        start,endを指定しなかった場合、
        2000-01-01から可能な限り最新のデータを取得する。
        """
        # barsデータを取得
        bar_alpaca_api_list = get_bar_alpaca_api_list(
            symbol=symbol,
            timeframe=depart_timeframe_to_alpaca_api(timeframe),
            adjustment=depart_adjustment_to_alpaca_api(adjustment),
            start=start,
            end=end
        )
        # adapt: <= alpaca_api
        chart = arrive_chart_from_bar_alpaca_api_list(bar_alpaca_api_list)
        # adapt: => table
        bar_table_list = depart_chart_to_peewee_table_list(chart)
        # DBのモデルリストを保存
        self.cli_db.insert_models(bar_table_list)


    def fetch_chart_from_local(
            self,
            symbol: str,
            timeframe: Timeframe,
            adjustment: Adjustment,
            start: datetime = datetime(2000, 1, 1),
            end: datetime = datetime.now()
    ) -> None:
        """
        ローカルのDBから指定されたシンボルのbarを取得する。

        デフォルトの取得範囲は2000-01-01~now。
        """
        # 取得に必要なqueryを作成
        query = get_query_select_bar_alpaca(
            symbol=symbol,
            timeframe=timeframe,
            adjustment=adjustment,
            start=start,
            end=end
        )
        # barデータをDBから取得
        bar_list_peewee_table = self.cli_db.exec_query(query)
        # 取得物をドメイン層のbarモデルのリストに変換して返す
        return arrive_chart_from_peewee_table(bar_list_peewee_table)
