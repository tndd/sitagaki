from typing import List

from domain.materia.bar.model import Adjustment, Bar, Chart, Timeframe
from infra.api.alpaca.historical import Bar as BarAlpacaApi
from infra.db.table.bar import TableBarAlpaca


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


def arrive_chart_from_alpaca_api_list(
        bars_alpaca_api: List[BarAlpacaApi],
        adjustment: Adjustment,
        timeframe: Timeframe
) -> Chart:
    """
    Chart:
        AlpacaAPI<List> -> Domain
    """
    bars = [arrive_bar_from_alpaca_api(bar) for bar in bars_alpaca_api]
    symbol = bars_alpaca_api[0].symbol
    return Chart(
        symbol=symbol,
        timeframe=timeframe,
        adjustment=adjustment,
        bars=bars
    )


def arrive_bar_from_peewee_table(bar_peewee_table: TableBarAlpaca) -> Bar:
    """
    Bar:
        Peewee Table -> Domain
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


def arrive_bar_list_from_peewee_table(bars_peewee_table: List[TableBarAlpaca]) -> List[Bar]:
    """
    Bar<List>:
        Peewee Table -> Domain
    """
    return [arrive_bar_from_peewee_table(bar) for bar in bars_peewee_table]
