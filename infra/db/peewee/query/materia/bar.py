from datetime import datetime

from sqlmodel import between, select
from sqlmodel.sql.expression import SelectOfScalar

from domain.materia.bar.model import Timeframe
from infra.db.peewee.table.bar import TblBarDayAlpaca, TblBarHourAlpaca, TblBarMinAlpaca


def get_stmt_select_bar(
        symbol: str,
        timeframe: Timeframe,
        start: datetime,
        end: datetime
) -> SelectOfScalar:
    """
    指定されたtimeframeの
    特定のシンボルのstart~endの間のbarデータを取得する。
    """
    if start > end:
        # 開始日が終了日より前であることを確認
        raise ValueError("start must be before end")
    # 時間軸によるモデルの選択
    bar_model = None
    if timeframe == Timeframe.MIN:
        bar_model = TblBarMinAlpaca
    elif timeframe == Timeframe.HOUR:
        bar_model = TblBarHourAlpaca
    elif timeframe == Timeframe.DAY:
        bar_model = TblBarDayAlpaca
    else:
        raise ValueError(f"Invalid timeframe: {timeframe}")
    # 条件指定のステートメント作成
    stmt = select(bar_model) \
        .where(bar_model.symbol == symbol) \
        .where(between(bar_model.timestamp, start, end))
    return stmt