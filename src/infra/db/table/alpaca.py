from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


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


class TblBarMin(TblBarBase, table=True):
    __tablename__ = "alpaca.bar_min"


class TblBarHour(TblBarBase, table=True):
    __tablename__ = "alpaca.bar_hour"


class TblBarDay(TblBarBase, table=True):
    __tablename__ = "alpaca.bar_day"
