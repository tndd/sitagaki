from datetime import datetime
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


class TblBarBase(SQLModel):
    """
    Barという一般的なテーブル定義。
    ここから一分足や１時間足といった派生モデルができる。
    """
    symbol: str = Field(primary_key=True)
    timestamp: datetime = Field(primary_key=True)
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: Optional[float] = None
    vwap: Optional[float] = None


class TblBarMinAlpaca(TblBarBase, table=True):
    __tablename__ = "bar_min_alpaca"


class TblBarHourAlpaca(TblBarBase, table=True):
    __tablename__ = "bar_hour_alpaca"


class TblBarDayAlpaca(TblBarBase, table=True):
    __tablename__ = "bar_day_alpaca"
