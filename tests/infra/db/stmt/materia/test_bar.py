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

    条件:
        - シンボルが"AAPL"
        - 日付については全ての範囲を網羅する2000-01-01~nowとする。

    期待される結果:
        1. 取得件数は３件
        2. シンボルが"AAPL"のbarのみ取得
    """
    stmt_1 = get_stmt_select_bar(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        start=datetime(2000, 1, 1),
        end=datetime.now()
    )
    bars_result_1 = test_sqlm_cli.select_models(stmt_1)
    # 1-1 取得件数は３件
    assert len(bars_result_1) == 3
    # 1-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars_result_1)

    """
    case2: シンボルと時間軸による絞り込み

    条件:
        - シンボルが"AAPL"
        - 時間軸が"DAY"
        - 日付が2024-01-02から2024-01-04の間

    期待される結果:
        1. 取得件数は以下の日付の2件
            - timestamp=datetime(2024, 1, 2, 5, 0, 0)
            - timestamp=datetime(2024, 1, 3, 5, 0, 0)
        2. シンボルが"AAPL"のbarのみ取得
        3. 日付が2024-01-02から2024-01-04の間のbarのみ取得
    """
    stmt_2 = get_stmt_select_bar(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        start=datetime(2024, 1, 2),
        end=datetime(2024, 1, 4)
    )
    bars_result_2 = test_sqlm_cli.select_models(stmt_2)
    # 2-1 取得件数は以下の日付の2件
    assert len(bars_result_2) == 2
    # 2-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars_result_2)
    # 2-3 日付が2024-01-02から2024-01-04の間のbarのみ取得
    assert all(datetime(2024, 1, 2) <= bar.timestamp <= datetime(2024, 1, 4) for bar in bars_result_2)