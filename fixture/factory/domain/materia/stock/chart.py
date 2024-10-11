from datetime import datetime

from src.domain.materia.stock.chart.const import Adjustment, Timeframe
from src.domain.materia.stock.chart.model import Bar, Chart


def generate_bar() -> Bar:
    return Bar(
        timestamp=datetime(2024, 1, 2, 5, 0, 0),
        open=187.15,
        high=188.44,
        low=183.885,
        close=185.64,
        volume=114514.305358,
        trade_count=1009074.0,
        vwap=185.937347
    )


def generate_chart(
        symbol: str = "MOCKSYMBOL_94CE5395",
        timeframe: Timeframe = Timeframe.DAY,
        adjustment: Adjustment = Adjustment.RAW,
) -> Chart:
    """
    Chartデータ
        * symbol="MOCKSYMBOL_94CE5395"
        * 3件
        * adjustment="RAW"
        * timeframe="DAY"
        * 2024/1/2~2024/1/4の3日間
    """
    bars = [
        Bar(
            timestamp=datetime(2024, 1, 2, 5, 0, 0),
            open=187.15,
            high=188.44,
            low=183.885,
            close=185.64,
            volume=82496943.0,
            trade_count=1009074.0,
            vwap=185.937347
        ),
        Bar(
            timestamp=datetime(2024, 1, 3, 5, 0, 0),
            open=184.22,
            high=185.88,
            low=183.43,
            close=184.25,
            volume=58418916.0,
            trade_count=656956.0,
            vwap=184.322631
        ),
        Bar(
            timestamp=datetime(2024, 1, 4, 5, 0, 0),
            open=182.15,
            high=183.0872,
            low=180.88,
            close=181.91,
            volume=71992243.0,
            trade_count=712850.0,
            vwap=182.01753
        )
    ]
    return Chart(
        symbol=symbol,
        timeframe=timeframe,
        adjustment=adjustment,
        bars=bars
    )
