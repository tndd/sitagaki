from datetime import datetime

from domain.materia.bar.model import Adjustment, Bar, Chart, Timeframe


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


def generate_chart(
        symbol: str = "AAPL",
        timeframe: Timeframe = Timeframe.DAY,
        adjustment: Adjustment = Adjustment.RAW,
) -> Chart:
    """
    AAPL,MSFTの日足のデータ
        * adjustment="RAW"
        * timeframe="DAY"
        * AAPLについては、2024/1/2~2024/1/4の3日間。
        * MSFTについては、2024/1/2~2024/1/3の2日間。
    """
    bars = [
        Bar(
            symbol="AAPL",
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
            symbol="AAPL",
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
            symbol="AAPL",
            timestamp=datetime(2024, 1, 4, 5, 0, 0),
            open=182.15,
            high=183.0872,
            low=180.88,
            close=181.91,
            volume=71992243.0,
            trade_count=712850.0,
            vwap=182.01753
        ),
        Bar(
            symbol="MSFT",
            timestamp=datetime(2024, 1, 2, 5, 0, 0),
            open=181.99,
            high=182.76,
            low=180.17,
            close=181.18,
            volume=62339687.0,
            trade_count=681262.0,
            vwap=181.474375
        ),
        Bar(
            symbol="MSFT",
            timestamp=datetime(2024, 1, 3, 5, 0, 0),
            open=182.085,
            high=185.6,
            low=181.5,
            close=185.56,
            volume=59151720.0,
            trade_count=669304.0,
            vwap=184.370323
        )
    ]
    return Chart(
        symbol=symbol,
        timeframe=timeframe,
        adjustment=adjustment,
        bars=bars
    )
