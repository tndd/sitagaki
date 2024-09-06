from datetime import datetime

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import adapt_to_tbl_bar_alpaca_list
from infra.db.stmt.materia.bar import get_stmt_select_bar
from tests.utils.factory.domain.materia.bar import generate_bar_list


def test_get_stmt_select_bar(test_sqlm_cli):
    # 検証用のbarのリストをDBに用意
    bars = generate_bar_list()
    tbl_bars = adapt_to_tbl_bar_alpaca_list(bars, Timeframe.DAY)
    test_sqlm_cli.insert_models(tbl_bars)
    """
    case1: シンボルのみによる絞り込み

    期待される結果:
        - シンボルが"AAPL"のbarのみ取得
        - 取得件数は３件
    """
    stmt_1 = get_stmt_select_bar(
        symbol="AAPL",
        timeframe=Timeframe.DAY
    )
    bars_result_1 = test_sqlm_cli.select_models(stmt_1)
    assert len(bars_result_1) == 3
    assert all(bar.symbol == "AAPL" for bar in bars_result_1)

    """
    テスト2: シンボルと時間軸による絞り込み

    期待される結果:
        - シンボルが"AAPL"のbarのみ取得
        - 取得件数は３件
    """
    pass