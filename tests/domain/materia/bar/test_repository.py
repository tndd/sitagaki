from datetime import datetime, timedelta

import pytest

from domain.materia.bar.model import Timeframe
from infra.db.table.bar import TblBarDayAlpaca, TblBarMinAlpaca


@pytest.mark.ext
def test_pull_bars_from_online(test_bar_repo):
    # Note: 日足と分足のテストしかしてないので注意。
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
    # TODO: 実装
    pass