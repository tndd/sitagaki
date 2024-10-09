from alpaca.data.models import Bar as BarAlpacaApi

from domain.materia.stock.chart.const import Adjustment, Timeframe
from domain.materia.stock.chart.model import Chart
from infra.adapter.materia.stock.chart.adjustment import arrive_adjustment_from_table
from infra.adapter.materia.stock.chart.bar import (
    arrive_bar_from_alpaca_api,
    arrive_bar_from_table,
    depart_bar_to_table,
)
from infra.adapter.materia.stock.chart.timeframe import arrive_timeframe_from_table
from infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def arrive_chart_from_bar_alpaca_api_list(
        bars_alpaca_api: list[BarAlpacaApi],
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


def arrive_chart_from_table_list(bar_table_list: list[TableBarAlpaca]) -> Chart:
    """
    Chart:
        PeeweeTable<List> -> Domain
    """
    if not bar_table_list:
        raise ValueError("bars_tableが空です。")
    head_table = bar_table_list[0]
    symbol = str(head_table.symbol)
    timeframe = arrive_timeframe_from_table(head_table)
    adjustment = arrive_adjustment_from_table(head_table)
    bars = [arrive_bar_from_table(bar_table) for bar_table in bar_table_list]
    return Chart(
        symbol=symbol,
        timeframe=timeframe,
        adjustment=adjustment,
        bars=bars
    )


def depart_chart_to_table_list(chart: Chart) -> list[TableBarAlpaca]:
    """
    Chart -> PeeweeTable<List>
    """
    return [
        depart_bar_to_table(bar, chart.symbol, chart.timeframe, chart.adjustment)
        for bar in chart.bars
    ]