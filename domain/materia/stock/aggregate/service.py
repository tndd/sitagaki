from dataclasses import dataclass

from domain.materia.stock.chart.service import ChartService
from domain.materia.stock.ticker.service import TickerService


@dataclass
class StockAggService:
    chart_service: ChartService
    ticker_service: TickerService

    def update_charts(self) -> None:
        """
        銘柄データの更新

        基本的に全部更新する。
        引数指定で特定のグループの銘柄のみ全部更新という機能もつける。
        """
        pass

    def update_quotes(self) -> None:
        pass

    def update_trades(self) -> None:
        pass
