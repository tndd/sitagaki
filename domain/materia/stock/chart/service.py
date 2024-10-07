from dataclasses import dataclass, field

from domain.materia.stock.chart.model import Adjustment, Chart, Timeframe
from domain.materia.stock.chart.repository import ChartRepository


@dataclass
class ChartService:
    rp_chart: ChartRepository = field(default_factory=ChartRepository)

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

    def update_chart(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment
    ) -> None:
        """
        指定された条件でonline上から取得したチャートデータで、
        DB上のデータを更新する。

        DB上にある最新のtimestamp~可能な限り直近のデータ。
        """
        # 最新のtimestampを取得
        latest_timestamp = self.rp_chart.fetch_latest_timestamp_of_symbol(symbol, timeframe, adjustment)
        # それ以降のデータで更新
        self.rp_chart.store_chart_from_online(symbol, timeframe, adjustment, latest_timestamp)
