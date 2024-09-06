from datetime import datetime

from domain.materia.bar.model import Bar


def generate_bar() -> Bar:
    return Bar(
        symbol="AAPL",
        timestamp=datetime(2024, 1, 2, 5, 0, 0),
        open=187.15,
        high=188.44,
        low=183.885,
        close=185.64,
        volume=82496943.0,
        trade_count=1009074.0,
        vwap=185.937347
    )