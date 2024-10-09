from dataclasses import dataclass

from domain.materia.stock.chart.usecase import ChartUsecase
from domain.materia.stock.ticker.service import TickerService


@dataclass
class StockAggService:
    chart_service: ChartUsecase
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
