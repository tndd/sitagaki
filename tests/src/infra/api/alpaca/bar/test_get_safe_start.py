from datetime import datetime, timedelta

import pytest

from src.infra.api.alpaca.bar import ROOT_START_DATETIME, get_safe_start


def test_basic():
    """
    デフォルトのテスト

    startが未指定の場合、デフォルトの開始日時が返されることをテスト
    """
    start = None
    start_safe = get_safe_start(start)
    assert start_safe == ROOT_START_DATETIME


@pytest.mark.parametrize("start", [
    ROOT_START_DATETIME,
    datetime(2024,1,1),
    datetime(2024,1,1,1,1,1),
])
def test_range_root_to_now(start):
    """
    デフォルトの開始日時 ~ 現在時刻の間のstartが指定されている場合、
    その値が返されることをテスト
    """
    start_safe = get_safe_start(start)
    assert start_safe == start


@pytest.mark.parametrize('start', [
    ROOT_START_DATETIME - timedelta(days=1),
    ROOT_START_DATETIME - timedelta(minutes=1),
    ROOT_START_DATETIME - timedelta(milliseconds=1)
])
def test_before_root(start):
    """
    デフォルト開始日時よりも前の日時が入力された場合、
    startはデフォルト開始日時に設定される
    """
    start_safe =  get_safe_start(start)
    assert start_safe == ROOT_START_DATETIME


@pytest.mark.parametrize('start', [
    datetime.now() + timedelta(days=1),
    datetime.now() + timedelta(hours=1),
    datetime.now() + timedelta(minutes=1)
])
def test_future(start):
    """
    現在時刻よりも未来の日時が入力された場合、
    エラーが発生する。
    """
    with pytest.raises(ValueError, match="EID:3e00e226"):
        get_safe_start(start)
