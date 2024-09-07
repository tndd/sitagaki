from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import adapt_bar_list_domain_to_sqlm
from infra.db.sqlmodel import SQLModelClient
from tests.utils.factory.domain.materia.bar import generate_bar_list


def prepare_test_bars_on_db(
        sqlm_cli: SQLModelClient,
        timeframe: Timeframe
) -> None:
    """
    テスト用のbarデータをDBに登録する。

    登録内容については、generate_bar_list()の内容を参照。
    """
    bars = generate_bar_list()
    tbl_bars = adapt_bar_list_domain_to_sqlm(bars, timeframe)
    sqlm_cli.insert_models(tbl_bars)