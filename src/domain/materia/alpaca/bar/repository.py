from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from src.domain.materia.alpaca.bar.const import Adjustment, Timeframe
from src.domain.materia.alpaca.bar.model import Chart, SymbolTimestampSet
from src.infra.adapter.materia.alpaca.bar import (
    arrive_chart_from_bar_alpaca_api_list,
    arrive_chart_from_table_list,
    depart_adjustment_to_alpaca_api,
    depart_adjustment_to_table,
    depart_chart_to_table_list,
    depart_timeframe_to_alpaca_api,
    depart_timeframe_to_table,
)
from src.infra.api.alpaca.bar import AlpacaApiBarClient
from src.infra.db.peewee.client import CLI_PEEWEE, PeeweeClient
from src.infra.db.peewee.query.materia.stock.chart import get_query_select_bar_alpaca


@dataclass
class ChartRepository:
    cli_db: PeeweeClient
    cli_alpaca: AlpacaApiBarClient

    def store_chart_from_online(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        start: datetime | None = None,
        limit: int | None = None
    ) -> None:
        """
        指定されたシンボルのbarデータをonlineから取得し、DBに保存する。

        NOTE: endの指定がない理由
            基本的にオンライン上からデータを取得する場合、最新の日付までのデータを求めるから。
            endを指定したデータ取得の必要性を感じないし、いらない部分があるなら捨てればいい。
        """
        # barsデータを取得
        bar_alpaca_api_list = self.cli_alpaca.get_bar_alpaca_api_list(
            symbol=symbol,
            timeframe=depart_timeframe_to_alpaca_api(timeframe),
            adjustment=depart_adjustment_to_alpaca_api(adjustment),
            start=start,
            limit=limit
        )
        # adapt: <= alpaca_api
        chart = arrive_chart_from_bar_alpaca_api_list(
            bars_alpaca_api=bar_alpaca_api_list,
            adjustment=adjustment,
            timeframe=timeframe
        )
        # adapt: => peewee_table
        bar_table_list = depart_chart_to_table_list(chart)
        # DBのモデルリストを保存
        self.cli_db.insert_models(bar_table_list)

    def fetch_chart_from_local(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        start: datetime | None = None,
        end: datetime | None = None
    ) -> Chart:
        """
        ローカルのDBから指定されたシンボルのbarを取得する。

        不足データをオンラインから取得するみたいな気の利いた動作はさせていない。
        """
        # 取得に必要なqueryを作成
        query = get_query_select_bar_alpaca(
            symbol=symbol,
            timeframe=depart_timeframe_to_table(timeframe),
            adjustment=depart_adjustment_to_table(adjustment),
            start=start,
            end=end
        )
        try:
            # TableBarAlpacaのリストを取得
            bar_list_table = self.cli_db.exec_query_fetch(query)
            if not bar_list_table:
                """
                Barの取得件数が0件の場合、エラーを発生させる。
                おそらく条件の指定が間違っている。
                もし通信での失敗であれば0件という情報すら返らないだろう。
                """
                raise LookupError('Barの取得件数が0件')
            # 取得物をドメイン層のbarモデルのリストに変換して返す
            return arrive_chart_from_table_list(bar_list_table)
        except LookupError as le:
            # LATER: error_logという同じ実装を排除したい
            error_log = {
                'exception': le,
                'timestamp': datetime.now(),
                'args': locals()
            }
            """
            MEMO: raiseしたらまずいんじゃないのか？
                もしエラーが発生したならば、そこでプログラムをクラッシュさせるのではなく、
                エラーが起こったという情報をどこかに記録し、そのまま続行させるようにしなければ。
            """
            raise LookupError(error_log)
        except Exception as e:
            # LATER: エラーログをログファイルに出力する
            # LATER: 失敗時の処理を行う。ログ格納そして再実行のキューへの追加など。
            error_log = {
                'exception': e,
                'timestamp': datetime.now(),
                'args': locals()
            }
            raise Exception(error_log)

    def fetch_latest_timestamp_of_symbol_ls(
        self,
        symbols: Sequence[str],
        timeframe: Timeframe,
        adjustment: Adjustment
    ) -> SymbolTimestampSet:
        """
        指定されたシンボルリストに対する、
        DBに保存されている最新の日付を取得する。

        未取得の場合、Noneを返す。

        MEMO: この始まりのdatetime(2000,1,1)は定数化。
        MEMO: symbolは単発でもリストでも受け取れるようにしておく。
        """
        pass


# シングルトン
REPO_CHART = ChartRepository(
    cli_db=CLI_PEEWEE,
    cli_alpaca=AlpacaApiBarClient()
)
