from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from domain.materia.bar.model import Adjustment, Timeframe
from infra.adapter.materia.bar.depart import (
    depart_bar_to_peewee_table,
    depart_chart_to_peewee_table_list,
    depart_timeframe_to_alpaca_api,
)
from infra.db.table.bar import TableBarAlpaca
from tests.utils.factory.domain.materia.bar import generate_bar, generate_chart


def test_depart_timeframe_to_alpaca_api():
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.MIN), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.HOUR), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.DAY), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.WEEK), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.MONTH), TimeFrameAlpaca)


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
