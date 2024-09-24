from domain.materia.bar.model import Adjustment, Bar, Chart, Timeframe
from infra.adapter.materia.bar.arrive import (
    arrive_bar_from_alpaca_api,
    arrive_bar_from_peewee_table,
    arrive_bar_list_from_peewee_table,
    arrive_chart_from_alpaca_api_list,
)
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


def test_arrive_bar_list_from_peewee_table():
    """
    bar_peewee_table<List> => Bar<List>
    """
    pass
