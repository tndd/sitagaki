from datetime import datetime

from pydantic import BaseModel

from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe


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
    trade_count: float | None
    vwap: float | None


class Chart(BaseModel):
    """
    チャートデータを表す。

    メタ情報として、symbol,timeframe,adjustmentを持ち、
    barsにローソク足の集合を持つ。
    """
    symbol: str
    timeframe: Timeframe
    adjustment: Adjustment
    bars: list[Bar]


class SymbolTimestampSet(BaseModel):
    """
    シンボルのtimestampの集合を表す。

    メタ情報としてこの情報の出所としての
    timeframe,adjustmentを持つ。
    """
    timeframe: Timeframe
    adjustment: Adjustment
    data: dict[str, datetime | None]

    def get_update_target_symbols(
        self,
        cutoff: datetime = datetime.now()
    ) -> list[str]:
        """
        データ更新対象のシンボルを抽出する。

        > 対象となる基準
            timestampがNone
            timestampがcutoffよりも前の日付
        """
        update_target_symbols = [
            symbol
            for symbol, timestamp in self.data.items()
            if timestamp is None or timestamp < cutoff
        ]
        return update_target_symbols
