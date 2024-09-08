from dataclasses import dataclass

from infra.api.alpaca.trading import get_assets
from infra.db.sqlmodel import SQLModelClient


@dataclass
class TickerRepository:
    cli_db: SQLModelClient

    def pull_tickers_from_online(self) -> None:
        """
        全ての株式のリストをonlineから取得し、DBに保存する。
        """
        tickers_alpaca = get_assets()
        # TODO: 続きの実装
        # tickers_alpacaをドメインモデルに変換
        # tickersの保存