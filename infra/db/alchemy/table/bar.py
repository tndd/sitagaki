from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class TimeframeTable(Enum):
    MIN = 1
    HOUR = 2
    DAY = 4
    WEEK = 8
    MONTH = 16

class AdjustmentTable(Enum):
    RAW = 1
    SPLIT = 2
    DIVIDEND = 4
    ALL = 8



class TableBarAlpaca(DeclarativeBase):
    __tablename__ = "alpaca_bar"

    timestamp: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    symbol: Mapped[str] = mapped_column(String, primary_key=True)
    timeframe: Mapped[TimeframeTable] = mapped_column(Enum(TimeframeTable), primary_key=True)
    adjustment: Mapped[AdjustmentTable] = mapped_column(Enum(AdjustmentTable), primary_key=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float)
    trade_count: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    vwap: Mapped[Optional[float]] = mapped_column(Float, nullable=True)