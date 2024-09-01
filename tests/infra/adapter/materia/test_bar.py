from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar import (adapt_to_bar_list,
                                       adapt_to_tbl_bar_alpaca,
                                       adapt_to_timeframe_alpaca)
from infra.db.table.bar import (TblBarDayAlpaca, TblBarHourAlpaca,
                                TblBarMinAlpaca)
from tests.utils.factory.infra.api.alpaca import (MockBar, generate_bar_mock,
                                                  generate_barset_mock)


def test_adapt_to_timeframe_alpaca():
    """
    TimeFrameAlpacaはEnumであるため、isinstanceによる検証ができない。
    そのためvalueを比較するという形でテストを行っている。
    """
    assert adapt_to_timeframe_alpaca(Timeframe.MIN).value == TimeFrameAlpaca.Minute.value
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
    mock_bar = generate_bar_mock()
    # min
    tbl_bar_alpaca_min = adapt_to_tbl_bar_alpaca(mock_bar, Timeframe.MIN)
    assert isinstance(tbl_bar_alpaca_min, TblBarMinAlpaca)
    # hour
    tbl_bar_alpaca_hour = adapt_to_tbl_bar_alpaca(mock_bar, Timeframe.HOUR)
    assert isinstance(tbl_bar_alpaca_hour, TblBarHourAlpaca)
    # day
    tbl_bar_alpaca_day = adapt_to_tbl_bar_alpaca(mock_bar, Timeframe.DAY)
    assert isinstance(tbl_bar_alpaca_day, TblBarDayAlpaca)