from domain.materia.stock.historical.adapter.adjustment import (
    depart_adjustment_to_peewee_table,
)
from domain.materia.stock.historical.adapter.timeframe import (
    depart_timeframe_to_peewee_table,
)
from domain.materia.stock.historical.model import Adjustment, Bar, Timeframe
from infra.api.alpaca.bar import Bar as BarAlpacaApi
from infra.db.peewee.table.bar import TableBarAlpaca


def arrive_bar_from_alpaca_api(bar_alpaca_api: BarAlpacaApi) -> Bar:
    """
    Bar:
        Alpaca API -> Domain
    """
    return Bar(
        timestamp=bar_alpaca_api.timestamp,
        open=bar_alpaca_api.open,
        high=bar_alpaca_api.high,
        low=bar_alpaca_api.low,
        close=bar_alpaca_api.close,
        volume=bar_alpaca_api.volume,
        trade_count=bar_alpaca_api.trade_count,
        vwap=bar_alpaca_api.vwap,
    )


def arrive_bar_from_peewee_table(bar_peewee_table: TableBarAlpaca) -> Bar:
    """
    Bar:
        PeeweeTable -> Domain
    """
    return Bar(
        timestamp=bar_peewee_table.timestamp,
        open=bar_peewee_table.open,
        high=bar_peewee_table.high,
        low=bar_peewee_table.low,
        close=bar_peewee_table.close,
        volume=bar_peewee_table.volume,
        trade_count=bar_peewee_table.trade_count,
        vwap=bar_peewee_table.vwap,
    )


def depart_bar_to_peewee_table(
        bar: Bar,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment
) -> TableBarAlpaca:
    """
    Bar:
        Domain -> PeeweeTable
    """
    return TableBarAlpaca(
        symbol=symbol,
        timestamp=bar.timestamp,
        timeframe=depart_timeframe_to_peewee_table(timeframe),
        adjustment=depart_adjustment_to_peewee_table(adjustment),
        open=bar.open,
        high=bar.high,
        low=bar.low,
        close=bar.close,
        volume=bar.volume,
        vwap=bar.vwap,
    )
