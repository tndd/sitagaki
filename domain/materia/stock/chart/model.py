from datetime import datetime
from symtable import Symbol
from typing import Optional, Sequence

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
    bars: Sequence[Bar]


class SymbolTimestamp(BaseModel):
    """
    シンボルのtimestampを表す。
    """
    symbol: str
    timestamp: Optional[datetime]

    def is_update_target(self) -> bool:
        """
        アップデート対象であるかを判定する。

        timestampが今日の日付より古ければ対象と判定される。
        """
        if self.timestamp is None:
            # 日付なしならば、まだ情報取得が行われていないので対象
            return True
        return self.timestamp < datetime.now().date()


class SymbolTimestampSet(BaseModel):
    """
    シンボルのtimestampの集合を表す。

    メタ情報としてこの情報の出所としての
    timeframe,adjustmentを持つ。
    """
    timeframe: Timeframe
    adjustment: Adjustment
    timestamp_of_symbol_ls: Sequence[SymbolTimestamp]

    def get_update_target_symbols(self) -> Sequence[SymbolTimestamp]:
        """
        データ更新対象のシンボルを抽出する。
        """
        return [
            timestamp_of_symbol
            for timestamp_of_symbol in self.timestamp_of_symbol_ls
            if timestamp_of_symbol.is_update_target()
        ]
