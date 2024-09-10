from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from domain.materia.bar.model import Bar, Timeframe
from infra.adapter.materia.bar import (
    adapt_bar_alpaca_list_to_sqlm,
    adapt_bar_domain_to_sqlm,
    adapt_bar_list_domain_to_sqlm,
    adapt_bar_list_sqlm_to_domain,
    adapt_timeframe_domain_to_alpaca,
)
from infra.db.table.bar import TblBarDayAlpaca, TblBarHourAlpaca, TblBarMinAlpaca
from tests.utils.factory.domain.materia.bar import generate_bar_list
from tests.utils.factory.infra.api.alpaca import (
    generate_bar_alpaca,
    generate_bar_alpaca_list,
)
from tests.utils.factory.infra.db.table.bar import generate_tbl_bar_base_list


def test_adapt_timeframe_domain_to_alpaca():
    assert isinstance(adapt_timeframe_domain_to_alpaca(Timeframe.MIN), TimeFrameAlpaca)
    assert isinstance(adapt_timeframe_domain_to_alpaca(Timeframe.HOUR), TimeFrameAlpaca)
    assert isinstance(adapt_timeframe_domain_to_alpaca(Timeframe.DAY), TimeFrameAlpaca)
    assert isinstance(adapt_timeframe_domain_to_alpaca(Timeframe.WEEK), TimeFrameAlpaca)
    assert isinstance(adapt_timeframe_domain_to_alpaca(Timeframe.MONTH), TimeFrameAlpaca)


def test_adapt_bar_domain_to_sqlm():
    bar = generate_bar_alpaca()
    # min
    tbl_bar_alpaca_min = adapt_bar_domain_to_sqlm(bar, Timeframe.MIN)
    assert isinstance(tbl_bar_alpaca_min, TblBarMinAlpaca)
    # hour
    tbl_bar_alpaca_hour = adapt_bar_domain_to_sqlm(bar, Timeframe.HOUR)
    assert isinstance(tbl_bar_alpaca_hour, TblBarHourAlpaca)
    # day
    tbl_bar_alpaca_day = adapt_bar_domain_to_sqlm(bar, Timeframe.DAY)
    assert isinstance(tbl_bar_alpaca_day, TblBarDayAlpaca)


def test_adapt_bar_list_domain_to_sqlm():
    # WARN: 日足のテストのみ
    bars = generate_bar_list()
    tbl_bars_alpaca = adapt_bar_list_domain_to_sqlm(bars, Timeframe.DAY)
    assert isinstance(tbl_bars_alpaca, list)
    assert all(isinstance(tbl_bar, TblBarDayAlpaca) for tbl_bar in tbl_bars_alpaca)


def test_adapt_bar_list_sqlm_to_domain():
    # bars_sqlmの用意
    bars_sqlm_list = generate_tbl_bar_base_list()
    # adapt_bar_list_sqlm_to_domainによる変換
    bars = adapt_bar_list_sqlm_to_domain(bars_sqlm_list)
    # 変換結果のチェック
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)


def test_adapt_bar_alpaca_list_to_sqlm():
    # WARN: 日足のテストのみ
    bar_alpaca_list = generate_bar_alpaca_list()
    tbl_bars_alpaca = adapt_bar_alpaca_list_to_sqlm(bar_alpaca_list, Timeframe.DAY)
    assert isinstance(tbl_bars_alpaca, list)
    assert all(isinstance(tbl_bar, TblBarDayAlpaca) for tbl_bar in tbl_bars_alpaca)