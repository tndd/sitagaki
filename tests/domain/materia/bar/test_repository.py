from datetime import datetime, timedelta

import pytest
from sqlmodel import select

from domain.materia.bar.model import Adjustment, Chart, Timeframe
from tests.utils.dataload.materia.bar import prepare_test_bar_alpaca_on_db


@pytest.mark.online
def test_pull_bars_from_online(test_bar_repo):
    return # FIXME: テスト修正
    # WARN: 日足と分足のテストしかしてないので注意。
    """
    日足:
        負荷軽減のため、直近一週間分の情報を取得する。
    """
    one_week_ago = datetime.now() - timedelta(days=7)
    test_bar_repo.pull_bars_from_online(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        start=one_week_ago
    )
    stmt = select(TblBarDayAlpaca)
    bars_day = test_bar_repo.cli_db.select_models(stmt)
    assert isinstance(bars_day, list)
    assert all(isinstance(bar, TblBarDayAlpaca) for bar in bars_day)

    """
    分足:
        負荷軽減のため、特定の一日分の情報を取得する。
    """
    start_min = datetime(2024, 1, 16)
    end_min = start_min + timedelta(days=1)
    test_bar_repo.pull_bars_from_online(
        symbol="AAPL",
        timeframe=Timeframe.MIN,
        start=start_min,
        end=end_min
    )
    stmt = select(TblBarMinAlpaca)
    bars_min = test_bar_repo.cli_db.select_models(stmt)
    assert isinstance(bars_min, list)
    assert all(isinstance(bar, TblBarMinAlpaca) for bar in bars_min)


def test_fetch_chart_from_local(test_bar_repo):
    # データの準備
    prepare_test_bar_alpaca_on_db(test_bar_repo.cli_db)
    """
    case1: 時間軸省略時の取得動作確認
        デフォルト日付範囲については、全範囲を網羅できる2000-01-01~nowとしている。

    期待される結果:
        1. 取得件数は３件
    """
    chart = test_bar_repo.fetch_chart_from_local(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW
    )
    # 基本テスト: Barのリストが帰ってるか
    assert isinstance(chart, Chart)
    # 1-1 取得件数は３件
    assert len(chart.bars) == 3
    """
    FIXME: barの中身をテストするため、prepareの内容を調整
        Chartモデルへの変更に伴い、もうBarはsymbol,timeframe,adjustmentを持たない。
        そのため返される内容のテストは、その中身の値を吟味するしかない。
        それを実現するため、OHLCの値を特徴的にしてbarに一意性を持たせる形にする。

        それに伴い下のcaseも書き直し。
    """

    """
    case2: シンボルと時間軸による絞り込み

    条件:
        - シンボルが"AAPL"
        - 時間軸が"DAY"
        - 日付が2020-01-02から2020-01-03の間

    期待される結果:
        1. 取得件数は以下の日付の2件
        2. シンボルが"AAPL"のbarのみ取得
        3. 日付が2020-01-02から2020-01-03の間のbarのみ取得
    """
    bars = test_bar_repo.fetch_bars_from_local(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        start=datetime(2020, 1, 2),
        end=datetime(2020, 1, 3)
    )
    # 2-1 取得件数は以下の日付の2件
    assert len(bars) == 2
    # 2-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars)
    # 2-3 日付が2020-01-02から2020-01-03の間のbarのみ取得
    assert all(
        datetime(2020, 1, 2) <= bar.timestamp <= datetime(2020, 1, 3) for bar in bars
    )
