from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import (adapt_to_bar_list,
                                       adapt_to_tbl_bar_alpaca,
                                       adapt_to_timeframe_alpaca)
from tests.utils.factory.infra.alpaca import MockBar, generate_barset_mock


def test_adapt_to_timeframe_alpaca():
    """
    TimeFrameAlpacaはEnumであるため、isinstanceによる検証ができない。
    そのためvalueを比較するという形でテストを行っている。
    """
    assert adapt_to_timeframe_alpaca(Timeframe.MINUTE).value == TimeFrameAlpaca.Minute.value
    assert adapt_to_timeframe_alpaca(Timeframe.HOUR).value == TimeFrameAlpaca.Hour.value
    assert adapt_to_timeframe_alpaca(Timeframe.DAY).value == TimeFrameAlpaca.Day.value
    assert adapt_to_timeframe_alpaca(Timeframe.WEEK).value == TimeFrameAlpaca.Week.value
    assert adapt_to_timeframe_alpaca(Timeframe.MONTH).value == TimeFrameAlpaca.Month.value


def test_adapt_to_bar_list():
    mock_barset = generate_barset_mock()
    bars = adapt_to_bar_list(mock_barset)
    assert isinstance(bars, list)
    """
    # WARN: 擬似テスト

    MockBarについて:
        * MockBarはalpacaのBarとは継承関係にないクラス。
        * 本家のBarモデルの作成が困難であるためモックを使っている。
        * しかしMockBarはBarの要素を全て保有している。
        * このアダプタの変換テストにはモックであっても支障はない。
    """
    assert all(isinstance(bar, MockBar) for bar in bars)


def test_adapt_to_tbl_bar_alpaca():
    pass