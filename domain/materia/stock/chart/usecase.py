from dataclasses import dataclass, field
from typing import Sequence

from domain.materia.stock.chart.const import Adjustment, Timeframe
from domain.materia.stock.chart.model import Chart, SymbolTimestamp
from domain.materia.stock.chart.repository import ChartRepository


@dataclass
class ChartUsecase:
    rp_chart: ChartRepository = field(default_factory=ChartRepository)

    def update_chart(
        self,
        symbols: Sequence[str],
        timeframe: Timeframe,
        adjustment: Adjustment
    ) -> None:
        """
        指定された条件でonline上から取得したチャートデータで、
        DB上のデータを更新する。

        DB上にある最新のtimestamp~可能な限り直近のデータ。
        """
        # 最新のtimestampを取得
        symbol_timestamp_set = self.rp_chart.fetch_latest_timestamp_of_symbol_ls(symbols, timeframe, adjustment)
        # 更新対象のシンボルを抽出
        update_targets_symbol_timestamp = symbol_timestamp_set.get_update_target_symbols()
        # シンボルごとにデータ更新
        for symbol_timestamp in update_targets_symbol_timestamp:
            self.rp_chart.store_chart_from_online(
                symbol=symbol_timestamp.symbol,
                timeframe=timeframe,
                adjustment=adjustment,
                start=symbol_timestamp.timestamp
            )

    def fetch_chart(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        update_mode: bool = False
    ) -> Chart:
        """
        指定された条件のチャートデータを取得する。
        取得元はまずDBを探し、なければonlineから取得する。

        毎回更新が走るというのも面倒なので、
        デフォルトでは更新モードをfalseにし、通信が走らないようにする。
        """
        # update_modeがtrueなら、データを最新にする
        if update_mode:
            self.update_chart(symbol, timeframe, adjustment)
        # データの取得
        return self.rp_chart.fetch_chart_from_local(symbol, timeframe, adjustment)

