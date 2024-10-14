from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from fixture.infra.db.peewee.table.alpaca.bar import factory_table_bar_alpaca
from src.domain.materia.stock.chart.const import Timeframe
from src.infra.adapter.materia.stock.chart.timeframe import (
    arrive_timeframe_from_table,
    depart_timeframe_to_alpaca_api,
    depart_timeframe_to_table,
)
from src.infra.db.peewee.table.alpaca.bar import TimeframeTable


def test_arrive_timeframe_from_table():
    """
    bar_table => Timeframe

    timeframeがminであることが期待できる。
    """
    bar_table = factory_table_bar_alpaca()
    timeframe = arrive_timeframe_from_table(bar_table)
    assert isinstance(timeframe, Timeframe)
    assert timeframe == Timeframe.MIN


def test_depart_timeframe_to_alpaca_api():
    # minute
    assert depart_timeframe_to_alpaca_api(Timeframe.MIN).amount == TimeFrameAlpaca.Minute.amount
    assert depart_timeframe_to_alpaca_api(Timeframe.MIN).unit == TimeFrameAlpaca.Minute.unit
    # hour
    assert depart_timeframe_to_alpaca_api(Timeframe.HOUR).amount == TimeFrameAlpaca.Hour.amount
    assert depart_timeframe_to_alpaca_api(Timeframe.HOUR).unit == TimeFrameAlpaca.Hour.unit
    # day
    assert depart_timeframe_to_alpaca_api(Timeframe.DAY).amount == TimeFrameAlpaca.Day.amount
    assert depart_timeframe_to_alpaca_api(Timeframe.DAY).unit == TimeFrameAlpaca.Day.unit
    # week
    assert depart_timeframe_to_alpaca_api(Timeframe.WEEK).amount == TimeFrameAlpaca.Week.amount
    assert depart_timeframe_to_alpaca_api(Timeframe.WEEK).unit == TimeFrameAlpaca.Week.unit
    # month
    assert depart_timeframe_to_alpaca_api(Timeframe.MONTH).amount == TimeFrameAlpaca.Month.amount
    assert depart_timeframe_to_alpaca_api(Timeframe.MONTH).unit == TimeFrameAlpaca.Month.unit


def test_depart_timeframe_to_table():
    assert depart_timeframe_to_table(Timeframe.MIN) == TimeframeTable.MIN
    assert depart_timeframe_to_table(Timeframe.HOUR) == TimeframeTable.HOUR
    assert depart_timeframe_to_table(Timeframe.DAY) == TimeframeTable.DAY
    assert depart_timeframe_to_table(Timeframe.WEEK) == TimeframeTable.WEEK
    assert depart_timeframe_to_table(Timeframe.MONTH) == TimeframeTable.MONTH
