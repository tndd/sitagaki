from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import adapt_bar_list_domain_to_sqlm
from infra.db.sqlmodel import SQLModelClient
from tests.utils.factory.domain.materia.bar import generate_bar_list


def prepare_db_bar_day(sqlm_cli: SQLModelClient) -> None:
    """
    テスト用のbarデータをDBに登録する。

    登録されるのは日足のbarデータ。
    登録内容については、generate_bar_list()の内容を参照。
    """
    bars = generate_bar_list()
    tbl_bars = adapt_bar_list_domain_to_sqlm(bars, Timeframe.DAY)
    sqlm_cli.insert_models(tbl_bars)