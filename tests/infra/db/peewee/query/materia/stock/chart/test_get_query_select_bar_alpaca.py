from datetime import datetime

import pytest

import infra.db.peewee.client as peewee_cli
from infra.db.peewee.query.materia.stock.chart import get_query_select_bar_alpaca
from infra.db.peewee.table.alpaca.bar import AdjustmentTable, TimeframeTable
from tests.utils.generate.infra.db.peewee.bar import generate_table_bar_alpaca_list


def test_default():
    """
    シンボルのみによる絞り込み

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
    # データ用意
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    peewee_cli.insert_models(table_bar_alpaca_list)
    # データ取得
    query = get_query_select_bar_alpaca(
        symbol="AAPL",
        timeframe=TimeframeTable.DAY,
        adjustment=AdjustmentTable.RAW,
        start=datetime(2000, 1, 1),
        end=datetime.now()
    )
    bars_result_1 = peewee_cli.exec_query(query)
    # 1-1 取得件数は３件
    assert len(bars_result_1) == 3
    # 1-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars_result_1)


def test_symbol_and_timeframe():
    """
    シンボルと時間軸による絞り込み

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
    # データ用意
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    peewee_cli.insert_models(table_bar_alpaca_list)
    # データ取得
    query = get_query_select_bar_alpaca(
        symbol="AAPL",
        timeframe=TimeframeTable.DAY,
        adjustment=AdjustmentTable.RAW,
        start=datetime(2020, 1, 2),
        end=datetime(2020, 1, 3)
    )
    bars_result_2 = peewee_cli.exec_query(query)
    # 2-1 取得件数は以下の日付の2件
    assert len(bars_result_2) == 2
    # 2-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars_result_2)
    # 2-3 日付が2020-01-02から2020-01-03の間のbarのみ取得
    assert all(datetime(2020, 1, 2) <= bar.timestamp <= datetime(2020, 1, 3) for bar in bars_result_2)


def test_invalid_start_end():
    """
    終了日 < 開始日という逆転した日付指定を行うテスト。
    ValueErrorが発生することを確認する。
    """
    # データ用意
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    peewee_cli.insert_models(table_bar_alpaca_list)
    # データ取得
    with pytest.raises(ValueError) as e:
        get_query_select_bar_alpaca(
            symbol="AAPL",
            timeframe=TimeframeTable.DAY,
            adjustment=AdjustmentTable.RAW,
            start=datetime(2020, 1, 3),  # endより新しい
            end=datetime(2020, 1, 2)     # startより古い
        )
        assert str(e.value) == "start must be before end"