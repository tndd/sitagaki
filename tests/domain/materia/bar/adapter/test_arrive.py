from domain.materia.bar.adapter.arrive import (
    arrive_adjustment_from_peewee_table,
    arrive_bar_from_alpaca_api,
    arrive_bar_from_peewee_table,
    arrive_chart_from_alpaca_api_list,
    arrive_chart_from_peewee_table,
    arrive_timeframe_from_peewee_table,
)
from domain.materia.bar.model import Adjustment, Bar, Chart, Timeframe
from tests.utils.factory.infra.api.alpaca import (
    generate_bar_alpaca,
    generate_bar_alpaca_list,
)
from tests.utils.factory.infra.db.table.bar import (
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


def test_arrive_chart_from_alpaca_api_list():
    """
    bar_alpaca_api<List> => Chart
    """
    bar_alpaca_api_list = generate_bar_alpaca_list()
    chart = arrive_chart_from_alpaca_api_list(
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


def test_arrive_chart_from_peewee_table():
    """
    bar_peewee_table<List> => Bar<List>
    """
    bar_peewee_table_list = generate_table_bar_alpaca_list()
    chart = arrive_chart_from_peewee_table(bar_peewee_table_list)
    assert isinstance(chart, Chart)
    assert all(isinstance(bar, Bar) for bar in chart.bars)
