from datetime import datetime

import pytest

from fixture.infra.db.peewee.table.alpaca.bar import factory_table_bar_alpaca_list
from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe
from src.domain.origin.alpaca.bar.model import Chart
from src.domain.origin.alpaca.bar.repository import REPO_CHART


def test_basic():
    """
    時間軸省略時の取得動作確認
        デフォルト日付範囲については、全範囲を網羅できる2000-01-01~nowとしている。

    期待される結果:
        1. 取得件数は３件
        2. AAPL_L3_DAY_RAWのデータが取得されているか（volume=100,101,102）
    """
    # テストデータをDBに登録
    factory_table_bar_alpaca_list.load()
    # 取得
    chart = REPO_CHART.fetch_chart_from_local(
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


def test_date_range():
    """
    シンボルと時間軸による絞り込み

    条件:
        - シンボルが"AAPL"
        - 時間軸が"DAY"
        - 日付が2020-01-02から2020-01-03の間

    期待される結果:
        1. 取得件数は以下の日付の2件
        2. 日付が2020-01-02から2020-01-03の間のbarのみ取得
        3. volume=100のAAPL_L3_DAY_RAWのデータがスキップされているか
    """
    # テストデータをDBに登録
    factory_table_bar_alpaca_list.load()
    # 取得
    chart = REPO_CHART.fetch_chart_from_local(
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


def test_not_exist_symbol():
    """
    対象データが存在せず取得できない場合

    factory_table_bar_alpaca_listで取得される情報に
    以下のシンボルは存在しない。

    期待される結果:
        LookupErrorが発生

    条件:
        symbol = 'NOSYMBOL'
        timeframe = Timeframe.DAY
        adjustment = Adjustment.RAW
        2020-01-02 <= timestamp <= 2020-01-03の間

        NOSYMBOLというシンボルは存在しないためchartを取得することはできない。
        そのため検索結果が見つからないことを表すLookupErrorを返す。
    """
    # テストデータをDBに登録
    factory_table_bar_alpaca_list.load()
    # まずエラーが発生することを確認
    with pytest.raises(Exception) as excinfo:
        REPO_CHART.fetch_chart_from_local(
            symbol="NOSYMBOL",
            timeframe=Timeframe.DAY,
            adjustment=Adjustment.RAW,
            start=datetime(2020, 1, 2),
            end=datetime(2020, 1, 3)
        )
    # エラーがLookupErrorであることを確認
    assert excinfo.type == LookupError