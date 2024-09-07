from datetime import datetime, timedelta

import pytest

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import TblBarDayAlpaca, TblBarMinAlpaca
from tests.utils.fixture.materia.bar import prepare_bar_data


@pytest.mark.ext
def test_pull_bars_from_online(test_bar_repo):
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
    bars_day = test_bar_repo.cli_db.select_models(TblBarDayAlpaca)
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
    bars_min = test_bar_repo.cli_db.select_models(TblBarMinAlpaca)
    assert isinstance(bars_min, list)
    assert all(isinstance(bar, TblBarMinAlpaca) for bar in bars_min)


def test_fetch_bars_from_local(test_bar_repo):
    # データの準備
    prepare_bar_data(test_bar_repo.cli_db)
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
        start=datetime(2000, 1, 1),
        end=datetime.now()
    )
    # Barのリストが帰ってるか
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)
    # 1-1 取得件数は３件
    assert len(bars) == 3
    # 1-2 シンボルが"AAPL"のbarのみ取得
    assert all(bar.symbol == "AAPL" for bar in bars)