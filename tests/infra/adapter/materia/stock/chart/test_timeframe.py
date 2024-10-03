from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from domain.materia.stock.chart.model import Timeframe
from infra.adapter.materia.stock.chart.timeframe import (
    arrive_timeframe_from_peewee_table,
    depart_timeframe_to_alpaca_api,
    depart_timeframe_to_peewee_table,
)
from infra.db.peewee.table.bar import TimeframeTable
from tests.utils.mock.infra.db.peewee.bar import generate_table_bar_alpaca


def test_arrive_timeframe_from_peewee_table():
    """
    bar_peewee_table => Timeframe

    timeframeがminであることが期待できる。
    """
    bar_peewee_table = generate_table_bar_alpaca()
    timeframe = arrive_timeframe_from_peewee_table(bar_peewee_table)
    assert isinstance(timeframe, Timeframe)
    assert timeframe == Timeframe.MIN


def test_depart_timeframe_to_alpaca_api():
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.MIN), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.HOUR), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.DAY), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.WEEK), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.MONTH), TimeFrameAlpaca)


def test_depart_timeframe_to_peewee_table():
    assert depart_timeframe_to_peewee_table(Timeframe.MIN) == TimeframeTable.MIN
    assert depart_timeframe_to_peewee_table(Timeframe.HOUR) == TimeframeTable.HOUR
    assert depart_timeframe_to_peewee_table(Timeframe.DAY) == TimeframeTable.DAY
    assert depart_timeframe_to_peewee_table(Timeframe.WEEK) == TimeframeTable.WEEK
    assert depart_timeframe_to_peewee_table(Timeframe.MONTH) == TimeframeTable.MONTH
