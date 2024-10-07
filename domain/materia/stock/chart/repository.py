from datetime import datetime
from typing import Optional

from domain.materia.stock.chart.model import Adjustment, Chart, Timeframe
from infra.adapter.materia.stock.chart.adjustment import (
    depart_adjustment_to_alpaca_api,
    depart_adjustment_to_table,
)
from infra.adapter.materia.stock.chart.chart import (
    arrive_chart_from_bar_alpaca_api_list,
    arrive_chart_from_table_list,
    depart_chart_to_table_list,
)
from infra.adapter.materia.stock.chart.timeframe import (
    depart_timeframe_to_alpaca_api,
    depart_timeframe_to_table,
)
from infra.api.alpaca.bar import get_bar_alpaca_api_list
from infra.db.peewee.client import PeeweeClient
from infra.db.peewee.query.materia.stock.chart import get_query_select_bar_alpaca

cli_db = PeeweeClient()
def store_chart_from_online(
    symbol: str,
    timeframe: Timeframe,
    adjustment: Adjustment,
    start: datetime = datetime(2000, 1, 1),
    end: Optional[datetime] = None,
    limit: Optional[int] = None
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
    cli_db.insert_models(bar_table_list)

def fetch_chart_from_local(
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
        """
        例外処理はリポジトリで行う。

        例えば下のような検索結果０というのも本来は異常事態だ。

        だがデータ取得関数get_bar_alpaca_api_list()からすれば、
        条件に忠実に従い0件という結果を持ってきたという正常な振る舞いでしかない。

        しかし、この結果はリポジトリにとってはエラーとなる。
        リポジトリはプログラム側ではなくユーザー側の都合で例外を発生させる。
        だからdomain-infra間で例外に対する相違が生まれる。
        """
        # barデータをDBから取得
        bar_list_table = cli_db.exec_query(query)
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

def fetch_latest_timestamp_of_symbol(
    symbol: str,
    timeframe: Timeframe,
    adjustment: Adjustment
) -> datetime:
    """
    指定された条件のシンボルの、
    DBに保存されている最新の日付を取得する。

    未取得の場合、datetime(2000,1,1)を返す。

    MEMO: この始まりのdatetime(2000,1,1)は定数化しよう。
    """
    # TODO: 続きの実装
    pass
