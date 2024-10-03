from enum import Enum

from sqlalchemy import Column, DateTime, Enum, Float, String

from infra.db.alchemy.client import Base


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


class TableBarAlpaca(Base):
    __tablename__ = "bar_alpaca"

    timestamp = Column(DateTime, primary_key=True)
    symbol = Column(String, primary_key=True)
    timeframe = Column(Enum(TimeframeTable), primary_key=True)
    adjustment = Column(Enum(AdjustmentTable), primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    trade_count = Column(Float, nullable=True)
    vwap = Column(Float, nullable=True)
