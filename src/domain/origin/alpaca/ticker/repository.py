from dataclasses import dataclass

from src.domain.origin.alpaca.ticker.model import Sector, Ticker
from src.infra.api.alpaca.trade import get_assets


@dataclass
class TickerRepository:

    def pull_tickers_from_online(self) -> None:
        """
        全ての株式のリストをonlineから取得し、DBに保存する。
        """
        tickers_alpaca = get_assets()
        # LATER: ticker repository 続きの実装
        # tickers_alpacaをドメインモデルに変換
        # tickersの保存
        pass

    def fetch_tickers_from_local(self) -> list[Ticker]:
        """
        全ての株式のリストをDBから取得する。
        """
        pass

    def fetch_tickers_of_sector_from_local(self) -> list[str]:
        """
        WARN: 臨時実装

        セクターの株式リストをDBから取得する。
        """
        return [
            sector.key
            for sector in Sector
        ]
