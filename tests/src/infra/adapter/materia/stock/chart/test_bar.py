from src.domain.materia.stock.chart.const import Adjustment, Timeframe
from src.domain.materia.stock.chart.model import Bar
from src.infra.adapter.materia.stock.chart.bar import (
    arrive_bar_from_alpaca_api,
    arrive_bar_from_table,
    depart_bar_to_table,
)
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca
from tests.utils.factory.domain.materia.stock.chart import generate_bar
from tests.utils.factory.infra.api.alpaca.bar import generate_bar_alpaca
from tests.utils.factory.infra.db.peewee.bar import generate_table_bar_alpaca


def test_arrive_bar_from_alpaca_api():
    """
    bar_alpaca_api => Bar
    """
    bar_alpaca_api = generate_bar_alpaca()
    bar = arrive_bar_from_alpaca_api(bar_alpaca_api)
    assert isinstance(bar, Bar)


def test_arrive_bar_from_table():
    """
    bar_table => Bar
    """
    bar_table = generate_table_bar_alpaca()
    bar = arrive_bar_from_table(bar_table)
    assert isinstance(bar, Bar)


def test_depart_bar_to_table():
    bar = generate_bar()
    bar_table = depart_bar_to_table(
        bar,
        symbol="AAPL",
        timeframe=Timeframe.MIN,
        adjustment=Adjustment.RAW
    )
    assert isinstance(bar_table, TableBarAlpaca)