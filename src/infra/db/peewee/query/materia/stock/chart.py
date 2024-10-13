from datetime import datetime

from peewee import ModelSelect

from src.infra.db.peewee.table.alpaca.bar import (
    AdjustmentTable,
    TableBarAlpaca,
    TimeframeTable,
)


def get_query_select_bar_alpaca(
    symbol: str,
    timeframe: TimeframeTable,
    adjustment: AdjustmentTable,
    start: datetime | None = None,
    end: datetime | None = None
) -> ModelSelect:
    """
    指定されたsymbol,timeframe,adjustmentの条件に一致するbarデータを取得する。
    start~endの範囲内のbarデータを取得する。
    """
    # まずシンボル、Timeframe,Adjustmentでの絞り込み
    query_with_time = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == symbol,
        TableBarAlpaca.timeframe == timeframe,
        TableBarAlpaca.adjustment == adjustment,
    )
    # start,endの内容に合わせて絞り込み
    query_with_time = _filter_query_by_timerange(query_with_time, start, end)
    return query_with_time


def get_query_select_latest_timestamp_of_bar_alpaca(
    symbol: str,
    timeframe: TimeframeTable,
    adjustment: AdjustmentTable
) -> ModelSelect:
    """
    指定されたtimeframe,adjustmentのシンボルの最新の日付を取得
    """
    query = TableBarAlpaca.select(
        TableBarAlpaca.timestamp
    ).where(
        TableBarAlpaca.symbol == symbol,
        TableBarAlpaca.timeframe == timeframe,
        TableBarAlpaca.adjustment == adjustment
    ).order_by(
        TableBarAlpaca.timestamp.desc()
    ).limit(1)
    return query


### Helper
def _filter_query_by_timerange(
    query: ModelSelect,
    start: datetime | None,
    end: datetime | None
) -> ModelSelect:
    # startがendよりも新しい場合はエラー
    if start is not None and end is not None and start > end:
        raise ValueError("startがendよりも新しい日付です。EID:45b0f55b")
    # start,endの内容に合わせ、query絞り込み
    if start is not None and end is not None:
        query = query.where(TableBarAlpaca.timestamp.between(start, end))
    elif start is not None:
        query = query.where(TableBarAlpaca.timestamp >= start)
    elif end is not None:
        query = query.where(TableBarAlpaca.timestamp <= end)
    return query
