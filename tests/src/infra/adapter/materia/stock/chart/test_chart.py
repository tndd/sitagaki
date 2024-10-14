from fixture.domain.materia.stock.chart import factory_chart
from fixture.infra.api.alpaca.bar import factory_bar_alpaca_list
from fixture.infra.db.peewee.table.alpaca.bar import factory_table_bar_alpaca_list
from src.domain.materia.alpaca.bar.const import Adjustment, Timeframe
from src.domain.materia.alpaca.bar.model import Bar, Chart
from src.infra.adapter.materia.stock.chart.chart import (
    arrive_chart_from_bar_alpaca_api_list,
    arrive_chart_from_table_list,
    depart_chart_to_table_list,
)
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_arrive_chart_from_bar_alpaca_api_list():
    """
    bar_alpaca_api<List> => Chart
    """
    bar_alpaca_api_list = factory_bar_alpaca_list()
    chart = arrive_chart_from_bar_alpaca_api_list(
        bars_alpaca_api=bar_alpaca_api_list,
        adjustment=Adjustment.RAW,
        timeframe=Timeframe.MIN,
    )
    assert isinstance(chart, Chart)


def test_arrive_chart_from_table_list():
    """
    bar_table<List> => Bar<List>
    """
    bar_table_list = factory_table_bar_alpaca_list()
    chart = arrive_chart_from_table_list(bar_table_list)
    assert isinstance(chart, Chart)
    assert all(isinstance(bar, Bar) for bar in chart.bars)


def test_depart_chart_to_table_list():
    """
    変換確認
        Chart -> PeeweeTable<List>
    """
    chart = factory_chart()
    bar_list_table = depart_chart_to_table_list(chart)
    assert isinstance(bar_list_table, list)
    assert all(isinstance(bar_table, TableBarAlpaca) for bar_table in bar_list_table)