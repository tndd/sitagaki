from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

"""
TODO: barテーブル再検討
    timeframeとしてmin,hour,day,week,month.
    さらにadjustmentにraw,devided,splited,all.
    これらの組み合わせについて、すべてテーブルを作るのは悪手？
    余分なカラムは増えるが。

TODO: TblBarBaseの名称
    上の案を採用するのであれば、"TblBarAlpaca"という名称のほうが妥当。
    これはalpaca api barの要素を網羅するモデルであるため、
    それ以上の汎用性を持っていると誤解される命名は避けるべき。
"""

class TimeframeAlpaca(str, Enum):
    MIN = "min"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class AdjustmentAlpaca(str, Enum):
    RAW = "raw"
    DIVIDED = "divided"
    SPLIT = "split"
    ALL = "all"


class TblBarAlpaca(SQLModel, table=True):
    """
    AlpacaAPIのhistorical barに準拠したテーブル。
    """
    __tablename__ = "bar_alpaca"

    symbol: str = Field(primary_key=True)
    timestamp: datetime = Field(primary_key=True)
    timeframe: TimeframeAlpaca = Field(primary_key=True)
    adjustment: AdjustmentAlpaca = Field(primary_key=True)
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: Optional[float] = None
    vwap: Optional[float] = None
