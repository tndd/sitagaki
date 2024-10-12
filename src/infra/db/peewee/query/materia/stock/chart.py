from datetime import datetime

from peewee import ModelSelect

from src.infra.api.alpaca.bar import get_safe_timerange
from src.infra.db.peewee.table.alpaca.bar import (
    AdjustmentTable,
    TableBarAlpaca,
    TimeframeTable,
)


def get_query_select_bar_alpaca(
    symbol: str,
    timeframe: TimeframeTable,
    adjustment: AdjustmentTable,
    start: datetime | None,
    end: datetime | None
) -> ModelSelect:
    """
    FIXME: endの指定廃止に伴うクエリ生成箇所の修正
        get_safe_timerange()のend廃止に伴い、
        このクエリ生成関数の修正も必要となる。

    指定されたsymbol,timeframe,adjustmentの条件に一致するbarデータを取得する。
    start~endの範囲内のbarデータを取得する。

    MEMO: get_safe_timerange()の使用について
        apiとクエリ作成は別物であるため、このようにapiのメソッドを使うというのは責任範囲を超えている気もする。
        しかしクエリとはapiから引っ張ってきたデータを取り出すためのものであるため、
        apiのメソッドでstart,endのバリデーションを行うことに合理性はある。
        一応垣根を越えたメソッドの利用であるためここにメモは残しておく。
    """
    time_range = get_safe_timerange(start, end)
    query = TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == symbol,
        TableBarAlpaca.timeframe == timeframe,
        TableBarAlpaca.adjustment == adjustment,
        TableBarAlpaca.timestamp.between(time_range.start, time_range.end)
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
