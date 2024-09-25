from datetime import datetime

from domain.materia.bar.model import Timeframe
from infra.db.stmt.materia.bar import get_stmt_select_bar
from tests.utils.fixture.domain.materia.bar import prepare_test_bars_on_db


def test_get_stmt_select_bar(test_sqlm_cli):
    # データ準備。日足テーブルで検証する。
    TIMEFRAME = Timeframe.DAY
    prepare_test_bars_on_db(test_sqlm_cli, TIMEFRAME)
    """
    case1: シンボルのみによる絞り込み

    条件:
        - シンボルが"AAPL"
        - (日付については全ての範囲を網羅できる2000-01-01~nowとする)

    期待される結果:
        1. 取得件数は３件
        2. シンボルが"AAPL"のbarのみ取得
    """
    stmt_1 = get_stmt_select_bar(
        symbol="AAPL",
        timeframe=TIMEFRAME,
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
        timeframe=TIMEFRAME,
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