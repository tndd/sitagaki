from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from domain.materia.stock.chart.const import Adjustment, Timeframe


class Bar(BaseModel):
    """
    ローソク足の一本を表す。
    """
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: Optional[float]
    vwap: Optional[float]


class Chart(BaseModel):
    """
    チャートデータを表す。

    メタ情報として、symbol,timeframe,adjustmentを持ち、
    barsにローソク足の集合を持つ。
    """
    symbol: str
    timeframe: Timeframe
    adjustment: Adjustment
    bars: List[Bar]


class TimestampOfSymbol(BaseModel):
    """
    シンボルのtimestampを表す。
    """
    symbol: str
    timestamp: Optional[datetime]

    def is_latest(self) -> bool:
        """
        最新のtimestampかどうかを返す。

        最新であるかどうかは、
        timestampが今日の日付より新しいかで判定する。
        """
        if self.timestamp is None:
            # 日付なしならば最新ではないのは確実
            return False
        return self.timestamp > datetime.now().date()

