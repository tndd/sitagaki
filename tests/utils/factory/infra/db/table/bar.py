from datetime import datetime

from infra.db.table.bar import TableBarAlpaca


def generate_table_bar_alpaca() -> TableBarAlpaca:
    """
    timeframe: 1 -> min
    adjustment: 1 -> raw
    """
    return TableBarAlpaca(
        symbol="AAPL",
        timestamp=datetime(2020, 1, 1),
        timeframe=1,
        adjustment=1,
        open=100.0,
        high=105.0,
        low=99.0,
        close=102.0,
        volume=1000,
        vwap=101.0,
    )


def generate_table_bar_alpaca_list() -> list[TableBarAlpaca]:
    """
    AAPL,GGOL２つの日足の集まり。
    2020-01-01 ~ 2020-01-03の範囲。

    AAPLは3件、GOOGは2件。
    そしてノイズとして月足のAAPLが1件。

    timeframe: 4 -> day
    adjustment: 1 -> raw
    """
    return [
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 1),
            timeframe=4,
            adjustment=1,
            open=100.0,
            high=105.0,
            low=99.0,
            close=102.0,
            volume=1000,
            vwap=101.0,
        ),
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 2),
            timeframe=4,
            adjustment=1,
            open=101.0,
            high=106.0,
            low=100.0,
            close=103.0,
            volume=1001,
            vwap=102.0,
        ),
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 3),
            timeframe=4,
            adjustment=1,
            open=102.0,
            high=107.0,
            low=101.0,
            close=104.0,
            volume=1002,
            vwap=103.0,
        ),
        TableBarAlpaca(
            symbol="GOOG",
            timestamp=datetime(2020, 1, 1),
            timeframe=4,
            adjustment=1,
            open=200.0,
            high=205.0,
            low=199.0,
            close=202.0,
            volume=2000,
            vwap=201.0,
        ),
        TableBarAlpaca(
            symbol="GOOG",
            timestamp=datetime(2020, 1, 2),
            timeframe=4,
            adjustment=1,
            open=201.0,
            high=206.0,
            low=200.0,
            close=203.0,
            volume=2001,
            vwap=202.0,
        ),
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 1),
            timeframe=16,
            adjustment=1,
            open=100.0,
            high=105.0,
            low=99.0,
        ),
    ]