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


def get_query_select_bar_alpaca_latest_timestamp_of_symbols(
    timeframe: TimeframeTable,
    adjustment: AdjustmentTable,
    symbols: list[str] | None = None
) -> ModelSelect:
    """
    指定されたtimeframe,adjustmentについて、
    渡されたシンボル一覧の最新取得日のモデルを返す

    > シンボルの指定がない場合
        DB状に存在する指定条件のシンボル全てを返す

    > 存在しないシンボルを指定した場合
        そのシンボルについては無視され結果は返らない
    """
    query = TableBarAlpaca.select(
        TableBarAlpaca.symbol,
        fn.MAX(TableBarAlpaca.timestamp)
    ).where(
        TableBarAlpaca.timeframe == timeframe,
        TableBarAlpaca.adjustment == adjustment
    )
    # シンボル指定がある場合、絞り込み処理を追加で行う
    if symbols is not None:
        query = query.where(TableBarAlpaca.symbol.in_(symbols))
    # groupby
    query = query.group_by(
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
