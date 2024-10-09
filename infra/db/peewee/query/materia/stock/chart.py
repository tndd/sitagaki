from datetime import datetime

from peewee import ModelSelect

from infra.db.peewee.table.alpaca.bar import (
    AdjustmentTable,
    TableBarAlpaca,
    TimeframeTable,
)


def get_query_select_bar_alpaca(
    symbol: str,
    timeframe: TimeframeTable,
    adjustment: AdjustmentTable,
    start: datetime,
    end: datetime
) -> ModelSelect:
    # TODO: Noneを受け入れられるように
    """
    指定されたsymbol,timeframe,adjustmentの条件に一致するbarデータを取得する。
    start~endの範囲内のbarデータを取得する。
    """
    if start > end:
        # 開始日が終了日より前であることを確認
        raise ValueError("start must be before end")
    query = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == symbol,
        TableBarAlpaca.timeframe == timeframe,
        TableBarAlpaca.adjustment == adjustment,
        TableBarAlpaca.timestamp.between(start, end)
    )
    return query


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
