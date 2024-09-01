from datetime import datetime, timedelta

import pytest

from domain.materia.bar.model import Timeframe
from infra.db.table.bar import TblBarDayAlpaca


@pytest.mark.ext
def test_pull_bars_from_online(test_bar_repo):
    """
    負荷軽減のため、直近一週間分の情報を取得する。
    """
    one_week_ago = datetime.now() - timedelta(days=7)
    test_bar_repo.pull_bars_from_online(
        symbol="AAPL",
        timeframe=Timeframe.DAY,
        start=one_week_ago
    )
    # 取得したデータのチェックする
    bars = test_bar_repo.cli_db.select_models(TblBarDayAlpaca)
    assert len(bars) > 0 # TODO: もう少し厳密にチェックする


def test_fetch_bars_from_local(test_bar_repo):
    # TODO: 実装
    pass