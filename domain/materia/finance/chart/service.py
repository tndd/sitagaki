from dataclasses import dataclass

from domain.materia.finance.chart.model import Adjustment, Chart, Timeframe
from domain.materia.finance.chart.repository import ChartRepository


@dataclass
class ChartService:
    chat_repo: ChartRepository

    def fetch_chart(
            self,
            symbol: str,
            timeframe: Timeframe,
            adjustment: Adjustment
        ) -> Chart:
        """
        指定された条件のチャートデータを取得する。
        取得元はまずDBを探し、なければonlineから取得する。
        """
        # まずデータを最新にする
        self.update_chart(symbol, timeframe, adjustment)
        # データの取得
        return self.chat_repo.fetch_chart_from_local(symbol, timeframe, adjustment)


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
        latest_timestamp = self.chat_repo.fetch_latest_timestamp_of_symbol(symbol, timeframe, adjustment)
        # それ以降のデータで更新
        self.chat_repo.store_chart_from_online(symbol, timeframe, adjustment, latest_timestamp)
