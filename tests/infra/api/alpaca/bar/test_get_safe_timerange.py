from datetime import datetime, timedelta

import pytest

from infra.api.alpaca.bar import (
    DELAY,
    ROOT_START_DATETIME,
    TimeRange,
    get_safe_timerange,
)


def test_default():
    """
    デフォルトのテスト

    start,endともにNoneを指定した場合も安全な日付が帰っているか
    """
    start = None
    end = None
    time_range = get_safe_timerange(start, end)
    assert isinstance(time_range, TimeRange)
    # 開始日時はROOT_START_DATETIME
    assert time_range.start == ROOT_START_DATETIME
    # 終了日時は今の時刻の15分前より以前
    assert time_range.end < datetime.now() - timedelta(minutes=DELAY)


@pytest.mark.parametrize(
    'start,end',
    [
        (datetime(2020, 1, 1), datetime(2000, 1, 1)),
        (datetime(2001, 1, 1), datetime(2001, 1, 1)),
    ]
)
def test_reverse_start_end(start, end):
    """
    startがendよりも新しい日付であった場合。
    全くの同時刻であった場合もエラーとする。

    0. 逆転
    1. 同じ日付
    """
    with pytest.raises(ValueError):
        get_safe_timerange(start, end)
