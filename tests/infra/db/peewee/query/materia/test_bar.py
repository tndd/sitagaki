from datetime import datetime

from domain.materia.finance.chart.model import Adjustment, Timeframe
from infra.db.peewee.query.materia.bar import get_query_select_bar_alpaca
from infra.db.peewee.table.bar import TableBarAlpaca
from tests.utils.dataload.materia.bar import prepare_test_bar_alpaca_on_db


def test_get_query_select_bar_alpaca(test_peewee_cli):
    prepare_test_bar_alpaca_on_db(test_peewee_cli)
    # case0: データが入ってるかの確認
    query_0 = TableBarAlpaca.select()
    assert len(query_0) == 10
    """
    case1: シンボルのみによる絞り込み

    条件:
        - シンボルが"AAPL"
        - timeframe=DAY (日足)
        - adjustment=RAW
        - (日付については全ての範囲を網羅できる2000-01-01~nowとする)

    期待される結果:
        1. 取得件数は３件
            "AAPL_L3_DAY_RAW"の内容が取得される。
        2. シンボルが"AAPL"のbarのみ取得
    """
    query_1 = get_query_select_bar_alpaca(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        start=datetime(2000, 1, 1),
        end=datetime.now()
    )
    bars_result_1 = test_peewee_cli.exec_query(query_1)
    # 1-1 取得件数は３件
    assert len(query_1) == 3
    # 1-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars_result_1)

    """
    case2: シンボルと時間軸による絞り込み

    条件:
        - シンボルが"AAPL"
        - timeframe=DAY (日足)
        - adjustment=RAW
        - 日付が2020-01-02から2020-01-03の間

    期待される結果:
        1. 取得件数は以下の日付の2件
                case1から2020-01-01の分が省かれる
        2. シンボルが"AAPL"のbarのみ取得
        3. 日付が2020-01-02から2020-01-03の間のbarのみ取得
    """
    query_2 = get_query_select_bar_alpaca(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        start=datetime(2020, 1, 2),
        end=datetime(2020, 1, 3)
    )
    bars_result_2 = test_peewee_cli.exec_query(query_2)
    # 2-1 取得件数は以下の日付の2件
    assert len(bars_result_2) == 2
    # 2-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars_result_2)
    # 2-3 日付が2020-01-02から2020-01-03の間のbarのみ取得
    assert all(datetime(2020, 1, 2) <= bar.timestamp <= datetime(2020, 1, 3) for bar in bars_result_2)
