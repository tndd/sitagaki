from typing import List

from pydantic import BaseModel

from domain.materia.stock.historical.model.adjustment import (
    Adjustment,
    arrive_adjustment_from_peewee_table,
)
from domain.materia.stock.historical.model.bar import (
    Bar,
    arrive_bar_from_alpaca_api,
    arrive_bar_from_peewee_table,
    depart_bar_to_peewee_table,
)
from domain.materia.stock.historical.model.timeframe import (
    Timeframe,
    arrive_timeframe_from_peewee_table,
)
from infra.api.alpaca.stock.bar import Bar as BarAlpacaApi
from infra.db.peewee.table.bar import TableBarAlpaca


class Chart(BaseModel):
    """
    チャートデータを表す。

    メタ情報として、symbol,timeframe,adjustmentを持ち、
    barsにローソク足の集合を持つ。
    """
    symbol: str
    timeframe: Timeframe
    adjustment: Adjustment
    bars: List[Bar]


def arrive_chart_from_bar_alpaca_api_list(
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


def arrive_chart_from_peewee_table_list(bars_peewee_table: List[TableBarAlpaca]) -> Chart:
    """
    Chart:
        PeeweeTable<List> -> Domain
    """
    if not bars_peewee_table:
        raise ValueError("bars_peewee_tableが空です。")
    symbol = bars_peewee_table[0].symbol
    timeframe = arrive_timeframe_from_peewee_table(bars_peewee_table[0])
    adjustment = arrive_adjustment_from_peewee_table(bars_peewee_table[0])
    bars = [arrive_bar_from_peewee_table(bar) for bar in bars_peewee_table]
    return Chart(
        symbol=symbol,
        timeframe=timeframe,
        adjustment=adjustment,
        bars=bars
    )


def depart_chart_to_peewee_table_list(chart: Chart) -> List[TableBarAlpaca]:
    """
    Chart -> PeeweeTable<List>
    """
    return [
        depart_bar_to_peewee_table(bar, chart.symbol, chart.timeframe, chart.adjustment)
        for bar in chart.bars
    ]
