from typing import List

from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import TableBarAlpaca


def arrive_bar_peewee_table(bar_peewee_table: TableBarAlpaca) -> Bar:
    """
    Bar:
        Peewee Table -> Domain
    """
    pass


def arrive_bar_list_peewee_table(bars_peewee_table: List[TableBarAlpaca]) -> List[Bar]:
    """
    Bar<List>:
        Peewee Table -> Domain
    """
    return [arrive_bar_peewee_table(bar) for bar in bars_peewee_table]
