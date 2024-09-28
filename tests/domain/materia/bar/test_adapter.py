from alpaca.data.requests import Adjustment as AdjustmentAlpaca
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from domain.materia.bar.adapter import (
    arrive_adjustment_from_peewee_table,
    arrive_bar_from_alpaca_api,
    arrive_bar_from_peewee_table,
    arrive_chart_from_bar_alpaca_api_list,
    arrive_chart_from_peewee_table_list,
    arrive_timeframe_from_peewee_table,
    depart_adjustment_to_alpaca_api,
    depart_adjustment_to_peewee_table,
    depart_bar_to_peewee_table,
    depart_chart_to_peewee_table_list,
    depart_timeframe_to_alpaca_api,
    depart_timeframe_to_peewee_table,
)
from domain.materia.bar.model import Adjustment, Bar, Chart, Timeframe
from infra.db.peewee.table.bar import TableBarAlpaca
from tests.utils.factory.domain.materia.bar import generate_bar, generate_chart
from tests.utils.factory.infra.api.alpaca import (
    generate_bar_alpaca,
    generate_bar_alpaca_list,
)
from tests.utils.factory.infra.db.peewee.bar import (
    generate_table_bar_alpaca,
    generate_table_bar_alpaca_list,
)


def test_arrive_bar_from_alpaca_api():
    """
    bar_alpaca_api => Bar
    """
    bar_alpaca_api = generate_bar_alpaca()
    bar = arrive_bar_from_alpaca_api(bar_alpaca_api)
    assert isinstance(bar, Bar)


def test_arrive_chart_from_bar_alpaca_api_list():
    """
    bar_alpaca_api<List> => Chart
    """
    bar_alpaca_api_list = generate_bar_alpaca_list()
    chart = arrive_chart_from_bar_alpaca_api_list(
        bars_alpaca_api=bar_alpaca_api_list,
        adjustment=Adjustment.RAW,
        timeframe=Timeframe.MIN,
    )
    assert isinstance(chart, Chart)


def test_arrive_bar_from_peewee_table():
    """
    bar_peewee_table => Bar
    """
    bar_peewee_table = generate_table_bar_alpaca()
    bar = arrive_bar_from_peewee_table(bar_peewee_table)
    assert isinstance(bar, Bar)


def test_arrive_timeframe_from_peewee_table():
    """
    bar_peewee_table => Timeframe

    timeframeがminであることが期待できる。
    """
    bar_peewee_table = generate_table_bar_alpaca()
    timeframe = arrive_timeframe_from_peewee_table(bar_peewee_table)
    assert isinstance(timeframe, Timeframe)
    assert timeframe == Timeframe.MIN


def test_arrive_adjustment_from_peewee_table():
    """
    bar_peewee_table => Adjustment

    adjustmentがrawであることが期待できる。
    """
    bar_peewee_table = generate_table_bar_alpaca()
    adjustment = arrive_adjustment_from_peewee_table(bar_peewee_table)
    assert isinstance(adjustment, Adjustment)
    assert adjustment == Adjustment.RAW


def test_arrive_chart_from_peewee_table_list():
    """
    bar_peewee_table<List> => Bar<List>
    """
    bar_peewee_table_list = generate_table_bar_alpaca_list()
    chart = arrive_chart_from_peewee_table_list(bar_peewee_table_list)
    assert isinstance(chart, Chart)
    assert all(isinstance(bar, Bar) for bar in chart.bars)


def test_depart_timeframe_to_alpaca_api():
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.MIN), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.HOUR), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.DAY), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.WEEK), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.MONTH), TimeFrameAlpaca)


def test_depart_adjustment_to_alpaca_api():
    assert depart_adjustment_to_alpaca_api(Adjustment.RAW) == AdjustmentAlpaca.RAW
    assert depart_adjustment_to_alpaca_api(Adjustment.SPLIT) == AdjustmentAlpaca.SPLIT
    assert depart_adjustment_to_alpaca_api(Adjustment.DIVIDEND) == AdjustmentAlpaca.DIVIDEND
    assert depart_adjustment_to_alpaca_api(Adjustment.ALL) == AdjustmentAlpaca.ALL


def test_depart_timeframe_to_peewee_table():
    assert depart_timeframe_to_peewee_table(Timeframe.MIN) == 1
    assert depart_timeframe_to_peewee_table(Timeframe.HOUR) == 2
    assert depart_timeframe_to_peewee_table(Timeframe.DAY) == 4
    assert depart_timeframe_to_peewee_table(Timeframe.WEEK) == 8
    assert depart_timeframe_to_peewee_table(Timeframe.MONTH) == 16


def test_depart_adjustment_to_peewee_table():
    assert depart_adjustment_to_peewee_table(Adjustment.RAW) == 1
    assert depart_adjustment_to_peewee_table(Adjustment.SPLIT) == 2
    assert depart_adjustment_to_peewee_table(Adjustment.DIVIDEND) == 4
    assert depart_adjustment_to_peewee_table(Adjustment.ALL) == 8


def test_depart_bar_to_peewee_table():
    bar = generate_bar()
    bar_table = depart_bar_to_peewee_table(
        bar,
        symbol="AAPL",
        timeframe=Timeframe.MIN,
        adjustment=Adjustment.RAW
    )
    assert isinstance(bar_table, TableBarAlpaca)


def test_depart_chart_to_peewee_table_list():
    """
    変換確認
        Chart -> PeeweeTable<List>
    """
    chart = generate_chart()
    bar_list_table = depart_chart_to_peewee_table_list(chart)
    assert isinstance(bar_list_table, list)
    assert all(isinstance(bar_table, TableBarAlpaca) for bar_table in bar_list_table)
