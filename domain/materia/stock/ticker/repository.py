from dataclasses import dataclass

from infra.db.sqlmodel import SQLModelClient

from infra.api.alpaca.trade import get_assets


@dataclass
class TickerRepository:
    cli_db: SQLModelClient

    def pull_tickers_from_online(self) -> None:
        """
        全ての株式のリストをonlineから取得し、DBに保存する。
        """
        tickers_alpaca = get_assets()
        # LATER: ticker repository 続きの実装
        # tickers_alpacaをドメインモデルに変換
        # tickersの保存