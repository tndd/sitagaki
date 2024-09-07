from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import adapt_to_tbl_bar_alpaca_list
from infra.db.sqlmodel import SqlModelClient
from tests.utils.factory.domain.materia.bar import generate_bar_list


def prepare_bar_data(sqlm_cli: SqlModelClient) -> None:
    """
    テスト用のbarデータをDBに登録する。

    登録されるのは日足のbarデータ。
    登録内容については、generate_bar_list()の内容を参照。
    """
    bars = generate_bar_list()
    tbl_bars = adapt_to_tbl_bar_alpaca_list(bars, Timeframe.DAY)
    sqlm_cli.insert_models(tbl_bars)