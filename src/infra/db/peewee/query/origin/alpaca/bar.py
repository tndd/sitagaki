from datetime import datetime

from peewee import ModelSelect, fn

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
    symbols: list[str],
    timeframe: TimeframeTable,
    adjustment: AdjustmentTable
) -> ModelSelect:
    """
    指定されたtimeframe,adjustmentについて、
    渡されたシンボル一覧の最新取得日のモデルを返す

    注意:
        存在しないシンボルについての結果は返らない。
    """
    query = TableBarAlpaca.select(
        TableBarAlpaca.symbol,
        fn.MAX(TableBarAlpaca.timestamp)
    ).where(
        TableBarAlpaca.symbol.in_(symbols),
        TableBarAlpaca.timeframe == timeframe,
        TableBarAlpaca.adjustment == adjustment
    ).group_by(
        TableBarAlpaca.symbol
    ).order_by(
        TableBarAlpaca.symbol
    )
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
