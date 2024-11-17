from dataclasses import dataclass
from typing import Sequence

from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe
from src.domain.origin.alpaca.bar.model import Chart
from src.domain.origin.alpaca.bar.repository import REPO_CHART, ChartRepository


@dataclass
class ChartUsecase:
    rp_chart: ChartRepository

    def update(
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
        symbol_timestamp_set = self.rp_chart.fetch_latest_symbol_timestamp_set(symbols, timeframe, adjustment)
        # 更新対象のシンボルを抽出
        update_target_symbols = symbol_timestamp_set.get_update_target_symbols()
        # シンボルごとにデータ更新
        # LATER: 並列化
        for symbol in update_target_symbols:
            self.rp_chart.store_chart_from_online(
                symbol=symbol,
                timeframe=timeframe,
                adjustment=adjustment,
                start=symbol.timestamp
            )

    def fetch(
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
            self.update(symbol, timeframe, adjustment)
        # データの取得
        return self.rp_chart.fetch_chart_from_local(symbol, timeframe, adjustment)


USE_CHART = ChartUsecase(
    rp_chart=REPO_CHART
)