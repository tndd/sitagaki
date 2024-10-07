from datetime import datetime

import pytest

from domain.materia.stock.chart.model import Adjustment, Chart, Timeframe
from domain.materia.stock.chart.repository import fetch_chart_from_local
from infra.db.peewee.client import PeeweeClient
from infra.db.peewee.table.alpaca.bar import TableBarAlpaca
from tests.utils.mock.infra.db.peewee.bar import generate_table_bar_alpaca_list

peewee_cli = PeeweeClient()

def _load_table_bar_alpaca_on_db():
    """
    BarデータをDBに登録する。
    """
    # TODO: データ作成関数の分離の検討
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    peewee_cli.insert_models(table_bar_alpaca_list)

### HELPER TEST
def test_load_table_bar_alpaca_on_db():
    """
    テスト用関数load_table_bar_alpaca_on_db()の動作確認
    """
    _load_table_bar_alpaca_on_db()
    result = TableBarAlpaca.select()
    # ファクトリのBar本数は10本
    assert len(result) == 10


### MAIN TEST
def test_default():
    """
    時間軸省略時の取得動作確認
        デフォルト日付範囲については、全範囲を網羅できる2000-01-01~nowとしている。

    期待される結果:
        1. 取得件数は３件
        2. AAPL_L3_DAY_RAWのデータが取得されているか（volume=100,101,102）
    """
    # テストデータをDBに登録
    _load_table_bar_alpaca_on_db()
    # 取得
    chart = fetch_chart_from_local(
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
    _load_table_bar_alpaca_on_db()
    # 取得
    chart = fetch_chart_from_local(
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

    load_table_bar_alpaca_on_db()で取得される情報に
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
    _load_table_bar_alpaca_on_db()
    # まずエラーが発生することを確認
    with pytest.raises(Exception) as excinfo:
        fetch_chart_from_local(
            symbol="NOSYMBOL",
            timeframe=Timeframe.DAY,
            adjustment=Adjustment.RAW,
            start=datetime(2020, 1, 2),
            end=datetime(2020, 1, 3)
        )
    # エラーがLookupErrorであることを確認
    assert excinfo.type == LookupError