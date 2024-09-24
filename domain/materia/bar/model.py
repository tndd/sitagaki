from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Timeframe(Enum):
    """
    どの時間におけるBarを表わしているのかを表す。
    """
    MIN = "Minute"
    HOUR = "Hour"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"


class Adjustment(Enum):
    """
    株価データの調整方法を表す。

        * RAW: 未調整の生データ。株式分割や配当などの企業アクションによる影響が反映されていない。
        * SPLIT: 株式分割のみ調整済み。株価と出来高が株式分割に応じて調整されている。
        * DIVIDEND: 配当のみ調整済み。過去の配当金額が株価から差し引かれている。
        * ALL: すべての調整が適用済み。株式分割と配当の両方が反映されており、長期的な価格比較に適している。

    これらの調整は、異なる時点の株価を正確に比較するために使用される。
    例えば、株式分割後に株価が半分になった場合、SPLIT調整済みデータでは
    分割前の株価も半分に調整されるため、連続的な価格推移を見ることができる。
    """
    RAW = 'R'
    SPLIT = 'S'
    DIVIDED = 'D'
    ALL = 'A'


class Bar(BaseModel):
    """
    ローソク足１本に当１本に当たるデータ。
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