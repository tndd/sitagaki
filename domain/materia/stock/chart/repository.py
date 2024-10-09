from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Sequence, TypeGuard

from domain.materia.stock.chart.const import Adjustment, Timeframe
from domain.materia.stock.chart.model import Chart, SymbolTimestampSet
from infra.adapter.materia.stock.chart import (
    arrive_chart_from_bar_alpaca_api_list,
    arrive_chart_from_table_list,
    depart_adjustment_to_alpaca_api,
    depart_adjustment_to_table,
    depart_chart_to_table_list,
    depart_timeframe_to_alpaca_api,
    depart_timeframe_to_table,
)
from infra.api.alpaca.bar import AlpacaApiBarClient
from infra.db.peewee.client import PeeweeClient
from infra.db.peewee.query.materia.stock.chart import get_query_select_bar_alpaca
from infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def is_type_table_bar_alpaca(
    seq: Sequence[Any]
) -> TypeGuard[Sequence[TableBarAlpaca]]:
    """
    リストの中身がTableBarAlpacaであるかを判定する。

    基本的に取得されるテーブルの型は全て同じであるため、
    型のチェックは初めの一つのみを検証する形式とする。
    """
    return len(seq) > 0 and isinstance(seq[0], TableBarAlpaca)


@dataclass
class ChartRepository:
    cli_db: PeeweeClient = field(default_factory=PeeweeClient)
    cli_alpaca: AlpacaApiBarClient = field(default_factory=AlpacaApiBarClient)

    def store_chart_from_online(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int | None = None
    ) -> None:
        # TODO: デフォルト引数変更につきテストの追加
        """
        指定されたシンボルのbarデータをonlineから取得し、DBに保存する。

        start,endを指定しなかった場合、
        2000-01-01から可能な限り最新のデータを取得する。
        """
        # barsデータを取得
        bar_alpaca_api_list = self.cli_alpaca.get_bar_alpaca_api_list(
            symbol=symbol,
            timeframe=depart_timeframe_to_alpaca_api(timeframe),
            adjustment=depart_adjustment_to_alpaca_api(adjustment),
            start=start,
            end=end,
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
        start: datetime = datetime(2000, 1, 1),
        end: datetime = datetime.now()
    ) -> Chart:
        """
        ローカルのDBから指定されたシンボルのbarを取得する。

        デフォルトの取得範囲は2000-01-01~now。
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
            if not is_type_table_bar_alpaca(bar_list_table):
                raise TypeError('取得したデータの型が"TableBarAlpaca"ではありません')
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
            NOTE: raiseしたらまずいんじゃないのか？
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
