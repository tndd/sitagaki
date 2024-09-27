from datetime import datetime, timedelta

import pytest
from sqlmodel import select

from domain.materia.bar.model import Adjustment, Bar, Timeframe
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


def test_fetch_bars_from_local(test_bar_repo):
    """
    Note: テスト内容がstmtのものとかなり重複している？

    ここまでテスト内容が重複しているならば、stmtのテストは省略すべきか？
    だがrepositoryは複数のstmtや変換などの処理も行っている総合テストという性質が強い。
    そのためstmtのテストは省略しないほうがいい気はする。
    """
    # データの準備
    prepare_test_bar_alpaca_on_db(test_bar_repo.cli_db)
    """
    case1: シンボルのみによる絞り込み

    条件:
        - シンボルが"AAPL"
        - (日付については全ての範囲を網羅できる2000-01-01~nowとする)

    期待される結果:
        1. 取得件数は３件
        2. シンボルが"AAPL"のbarのみ取得
    """
    bars = test_bar_repo.fetch_bars_from_local(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        start=datetime(2000, 1, 1),
        end=datetime.now()
    )
    # 基本テスト: Barのリストが帰ってるか
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)
    # 1-1 取得件数は３件
    assert len(bars) == 3
    # 1-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars)

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
    bars = test_bar_repo.fetch_bars_from_local(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        start=datetime(2024, 1, 2),
        end=datetime(2024, 1, 4)
    )
    # 2-1 取得件数は以下の日付の2件
    assert len(bars) == 2
    # 2-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars)
    # 2-3 日付が2024-01-02から2024-01-04の間のbarのみ取得
    assert all(
        datetime(2024, 1, 2) <= bar.timestamp <= datetime(2024, 1, 4) for bar in bars
    )