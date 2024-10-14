from fixture.domain.materia.stock.chart import factory_bar
from fixture.infra.api.alpaca.bar import factory_bar_alpaca
from fixture.infra.db.peewee.table.alpaca.bar import factory_table_bar_alpaca
from src.domain.materia.alpaca.bar.const import Adjustment, Timeframe
from src.domain.materia.alpaca.bar.model import Bar
from src.infra.adapter.materia.stock.chart.bar import (
    arrive_bar_from_alpaca_api,
    arrive_bar_from_table,
    depart_bar_to_table,
)
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_arrive_bar_from_alpaca_api():
    """
    bar_alpaca_api => Bar
    """
    bar_alpaca_api = factory_bar_alpaca()
    bar = arrive_bar_from_alpaca_api(bar_alpaca_api)
    assert isinstance(bar, Bar)


def test_arrive_bar_from_table():
    """
    bar_table => Bar
    """
    bar_table = factory_table_bar_alpaca()
    bar = arrive_bar_from_table(bar_table)
    assert isinstance(bar, Bar)


def test_depart_bar_to_table():
    bar = factory_bar()
    bar_table = depart_bar_to_table(
        bar,
        symbol="AAPL",
        timeframe=Timeframe.MIN,
        adjustment=Adjustment.RAW
    )
    assert isinstance(bar_table, TableBarAlpaca)