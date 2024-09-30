from datetime import datetime

import pytest

import domain.materia.finance.chart.repository as repository
from domain.materia.finance.chart.adapter.adjustment import (
    arrive_adjustment_from_peewee_table,
)
from domain.materia.finance.chart.adapter.timeframe import (
    arrive_timeframe_from_peewee_table,
)
from domain.materia.finance.chart.model import Adjustment, Chart, Timeframe
from infra.db.peewee.table.bar import TableBarAlpaca
from tests.utils.dataload.materia.bar import prepare_test_bar_alpaca_on_db


def test_mock_store_chart_from_online(test_peewee_cli, mock_get_barset_alpaca_api):
    """
    通信部分をモックにした簡易テスト
    """
    # Mock通信
    repository.store_chart_from_online(
        cli_db=test_peewee_cli,
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
    )
    bar_table_list = TableBarAlpaca.select()
    # データが存在すること
    assert bar_table_list.exists()
    # データがTableBarAlpacaであること
    assert all(isinstance(bar, TableBarAlpaca) for bar in bar_table_list)


@pytest.mark.online
def test_store_chart_from_online(test_peewee_cli):
    """
    モックを使わず、すべての組み合わせによる情報取得テストを行う
    """
    # timeframe X adjustmentの組み合わせを全通り試す
    for timeframe in Timeframe:
        for adjustment in Adjustment:
            repository.store_chart_from_online(
                cli_db=test_peewee_cli,
                symbol="AAPL",
                timeframe=timeframe,
                adjustment=adjustment,
                limit=5
            )
            bar_table_list = TableBarAlpaca.select()
            # 取得件数の確認
            assert len(bar_table_list) == 5
            # データ内容の検証
            assert all(
                isinstance(bar, TableBarAlpaca) and
                arrive_timeframe_from_peewee_table(bar) == timeframe and
                arrive_adjustment_from_peewee_table(bar) == adjustment
                for bar in bar_table_list
            )
            # LATER: 取得したbar_table_listの中身をログなどで確認できるようにする
            # データをクリア
            TableBarAlpaca.delete().execute()


def test_fetch_chart_from_local(test_peewee_cli):
    # データの準備
    prepare_test_bar_alpaca_on_db(test_peewee_cli)
    """
    case1: 時間軸省略時の取得動作確認
        デフォルト日付範囲については、全範囲を網羅できる2000-01-01~nowとしている。

    期待される結果:
        1. 取得件数は３件
        2. AAPL_L3_DAY_RAWのデータが取得されているか（volume=100,101,102）
    """
    chart = repository.fetch_chart_from_local(
        cli_db=test_peewee_cli,
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW
    )
    # 基本テスト: Barのリストが帰ってるか
    assert isinstance(chart, Chart)
    # 1-1 取得件数は３件
    assert len(chart.bars) == 3
    # 1-2 AAPL_L3_DAY_RAWのデータが取得されているか（volume=100,101,102）
    assert all(100 <= bar.volume <= 102 for bar in chart.bars)

    """
    case2: シンボルと時間軸による絞り込み

    条件:
        - シンボルが"AAPL"
        - 時間軸が"DAY"
        - 日付が2020-01-02から2020-01-03の間

    期待される結果:
        1. 取得件数は以下の日付の2件
        2. 日付が2020-01-02から2020-01-03の間のbarのみ取得
        3. volume=100のAAPL_L3_DAY_RAWのデータがスキップされているか
    """
    chart = repository.fetch_chart_from_local(
        cli_db=test_peewee_cli,
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        start=datetime(2020, 1, 2),
        end=datetime(2020, 1, 3)
    )
    # 2-1 取得件数は以下の日付の2件
    assert len(chart.bars) == 2
    # 2-2 日付が2020-01-02から2020-01-03の間のbarのみ取得
    assert all(
        datetime(2020, 1, 2) <= bar.timestamp <= datetime(2020, 1, 3) for bar in chart.bars
    )
    # 2-3 volume=100のAAPL_L3_DAY_RAWのデータがスキップされているか
    assert not any(bar.volume == 100 for bar in chart.bars)

    """
    case3: 取得できない場合

    条件:
        symbol = 'NOSYMBOL'
        timeframe = Timeframe.DAY
        adjustment = Adjustment.RAW
        2020-01-02 <= timestamp <= 2020-01-03の間

    期待される結果:
        LookupErrorが発生すること。

        NOSYMBOLというシンボルは存在しないためchartを取得することはできない。
        そのため検索結果が見つからないことを表すLookupErrorを返す。
    """
    with pytest.raises(Exception) as excinfo:
        chart = repository.fetch_chart_from_local(
            cli_db=test_peewee_cli,
            symbol="NOSYMBOL",
            timeframe=Timeframe.DAY,
            adjustment=Adjustment.RAW,
            start=datetime(2020, 1, 2),
            end=datetime(2020, 1, 3)
        )
        assert excinfo.exception == LookupError