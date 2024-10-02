from domain.materia.stock.chart.adapter.chart import (
    arrive_chart_from_bar_alpaca_api_list,
    arrive_chart_from_peewee_table_list,
    depart_chart_to_peewee_table_list,
)
from domain.materia.stock.chart.model import Adjustment, Bar, Chart, Timeframe
from infra.db.peewee.table.bar import TableBarAlpaca
from tests.utils.factory.domain.materia.stock.chart import generate_chart
from tests.utils.factory.infra.api.alpaca.bar import generate_bar_alpaca_list
from tests.utils.factory.infra.db.peewee.bar import generate_table_bar_alpaca_list


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


def test_arrive_chart_from_peewee_table_list():
    """
    bar_peewee_table<List> => Bar<List>
    """
    bar_peewee_table_list = generate_table_bar_alpaca_list()
    chart = arrive_chart_from_peewee_table_list(bar_peewee_table_list)
    assert isinstance(chart, Chart)
    assert all(isinstance(bar, Bar) for bar in chart.bars)


def test_depart_chart_to_peewee_table_list():
    """
    変換確認
        Chart -> PeeweeTable<List>
    """
    chart = generate_chart()
    bar_list_table = depart_chart_to_peewee_table_list(chart)
    assert isinstance(bar_list_table, list)
    assert all(isinstance(bar_table, TableBarAlpaca) for bar_table in bar_list_table)