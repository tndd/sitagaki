from datetime import datetime

from peewee import ModelSelect

from domain.materia.stock.chart.adapter.adjustment import (
    depart_adjustment_to_peewee_table,
)
from domain.materia.stock.chart.adapter.timeframe import (
    depart_timeframe_to_peewee_table,
)
from domain.materia.stock.chart.model import Adjustment, Timeframe
from infra.db.peewee.table.bar import TableBarAlpaca


def get_query_select_bar_alpaca(
    symbol: str,
    timeframe: Timeframe,
    adjustment: Adjustment,
    start: datetime,
    end: datetime
) -> ModelSelect:
    """
    指定されたsymbol,timeframe,adjustmentの条件に一致するbarデータを取得する。
    start~endの範囲内のbarデータを取得する。
    """
    if start > end:
        # 開始日が終了日より前であることを確認
        raise ValueError("start must be before end")
    query = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == symbol,
        TableBarAlpaca.timeframe == depart_timeframe_to_peewee_table(timeframe),
        TableBarAlpaca.adjustment == depart_adjustment_to_peewee_table(adjustment),
        TableBarAlpaca.timestamp.between(start, end)
    )
    return query


def get_query_select_latest_timestamp_of_bar_alpaca(
    symbol: str,
    timeframe: Timeframe,
    adjustment: Adjustment
) -> ModelSelect:
    """
    指定されたtimeframe,adjustmentのシンボルの最新の日付を取得
    """
    query = TableBarAlpaca.select(
        TableBarAlpaca.timestamp
    ).where(
        TableBarAlpaca.symbol == symbol,
        TableBarAlpaca.timeframe == depart_timeframe_to_peewee_table(timeframe),
        TableBarAlpaca.adjustment == depart_adjustment_to_peewee_table(adjustment)
    ).order_by(
        TableBarAlpaca.timestamp.desc()
    ).limit(1)
    return query
