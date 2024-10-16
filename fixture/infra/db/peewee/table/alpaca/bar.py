from datetime import datetime
from random import shuffle

from numpy import insert

from fixture.infra.db.peewee.table.decorator import insertable
from src.infra.db.peewee.table.alpaca.bar import (
    AdjustmentTable,
    TableBarAlpaca,
    TimeframeTable,
)


@insertable
def factory_table_bar_alpaca(
    symbol: str = "AAPL",
    timeframe: TimeframeTable = TimeframeTable.MIN,
    adjustment: AdjustmentTable = AdjustmentTable.RAW,
    timestamp: datetime = datetime(2020, 1, 1),
) -> TableBarAlpaca:
    """
    AAPL,MIN,RAWのBarテーブルデータを生成する。
    """
    return TableBarAlpaca(
        symbol=symbol,
        timestamp=timestamp,
        timeframe=timeframe,
        adjustment=adjustment,
        open=100.0,
        high=105.0,
        low=99.0,
        close=102.0,
        volume=1000,
        vwap=101.0,
    )


@insertable
def factory_table_bar_alpaca_list() -> list[TableBarAlpaca]:
    """
    AAPL,GOOGのテーブルデータを生成する。

    データ内容
        AAPL_L3_DAY_RAW = 3件:
            symbol: AAPL
            日付: 2020-01-01 ~ 2020-01-03
            timeframe: 日足 = 4
            adjustment: raw = 1
            volume = 100 ~ 199
        AAPL_L3_MIN_RAW = 3件:
            symbol: AAPL
            日付: 2020-01-01 ~ 2020-01-03
            timeframe: 分足 = 1
            adjustment: raw = 1
            volume = 200 ~ 299
        AAPL_L2_MONTH_ALL = 2件:
            symbol: AAPL
            日付: 2020-01-01 ~ 2020-01-02
            timeframe: 月足 = 16
            adjustment: all = 8
            volume = 300 ~ 399
        GOOG_L2_DAY_RAW = 2件:
            symbol: GOOG
            日付: 2020-01-01 ~ 2020-01-02
            timeframe: 日足 = 4
            adjustment: raw = 1
            volume = 400 ~ 499
    """
    AAPL_L3_DAY_RAW = [
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 1),
            timeframe=TimeframeTable.DAY,
            adjustment=AdjustmentTable.RAW,
            open=100.0,
            high=105.0,
            low=99.0,
            close=102.0,
            volume=100,
            vwap=101.0,
        ),
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 2),
            timeframe=TimeframeTable.DAY,
            adjustment=AdjustmentTable.RAW,
            open=101.0,
            high=106.0,
            low=100.0,
            close=103.0,
            volume=101,
            vwap=102.0,
        ),
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 3),
            timeframe=TimeframeTable.DAY,
            adjustment=AdjustmentTable.RAW,
            open=102.0,
            high=107.0,
            low=101.0,
            close=104.0,
            volume=102,
            vwap=103.0,
        )
    ]
    AAPL_L3_MIN_RAW = [
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 1),
            timeframe=TimeframeTable.MIN,
            adjustment=AdjustmentTable.RAW,
            open=100.0,
            high=105.0,
            low=99.0,
            close=102.0,
            volume=200,
            vwap=101.0,
        ),
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 2),
            timeframe=TimeframeTable.MIN,
            adjustment=AdjustmentTable.RAW,
            open=101.0,
            high=106.0,
            low=100.0,
            close=103.0,
            volume=201,
            vwap=102.0,
        ),
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 3),
            timeframe=TimeframeTable.MIN,
            adjustment=AdjustmentTable.RAW,
            open=102.0,
            high=107.0,
            low=101.0,
            close=104.0,
            volume=202,
            vwap=103.0,
        )
    ]
    AAPL_L2_MONTH_ALL = [
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 1),
            timeframe=TimeframeTable.MONTH,
            adjustment=AdjustmentTable.ALL,
            open=100.0,
            high=105.0,
            low=99.0,
            close=102.0,
            volume=300,
            vwap=101.0,
        ),
        TableBarAlpaca(
            symbol="AAPL",
            timestamp=datetime(2020, 1, 2),
            timeframe=TimeframeTable.MONTH,
            adjustment=AdjustmentTable.ALL,
            open=100.0,
            high=105.0,
            low=99.0,
            close=102.0,
            volume=301,
            vwap=101.0,
        )
    ]
    GOOG_L2_DAY_RAW = [
        TableBarAlpaca(
            symbol="GOOG",
            timestamp=datetime(2020, 1, 1),
            timeframe=TimeframeTable.DAY,
            adjustment=AdjustmentTable.RAW,
            open=200.0,
            high=205.0,
            low=199.0,
            close=202.0,
            volume=400,
            vwap=201.0,
        ),
        TableBarAlpaca(
            symbol="GOOG",
            timestamp=datetime(2020, 1, 2),
            timeframe=TimeframeTable.DAY,
            adjustment=AdjustmentTable.RAW,
            open=201.0,
            high=206.0,
            low=200.0,
            close=203.0,
            volume=401,
            vwap=202.0,
        )
    ]
    # 全てを結合し、１つのリストにして返す
    return (
        AAPL_L3_DAY_RAW +
        AAPL_L3_MIN_RAW +
        AAPL_L2_MONTH_ALL +
        GOOG_L2_DAY_RAW
    )


@insertable
def factory_table_bar_alpaca_list_times_shuffle() -> list[TableBarAlpaca]:
    """
    AAPL, GOOGのデータテーブルを生成
    timeframe=DAY, adjustment=RAWに固定。
    日付の違いに特化して生成を行う。

    合計10件
    """
    def _create_bar_data(symbol, year, month, day_start):
        """
        指定した日付から5日間のデータを生成する。
        """
        return [
            factory_table_bar_alpaca(
                symbol=symbol,
                timeframe=TimeframeTable.DAY,
                adjustment=AdjustmentTable.RAW,
                timestamp=datetime(year, month, day)
            )
            for day in range(day_start, day_start + 5)
        ]

    AAPL = _create_bar_data("AAPL", 2020, 1, 1)
    GOOG = _create_bar_data("GOOG", 2021, 1, 1)
    # テーブルの並びはランダムにシャッフルして返す
    tables = AAPL + GOOG
    shuffle(tables)
    return tables


@insertable
def factory_table_bar_alpaca_latest_timestamps() -> list[TableBarAlpaca]:
    """
    複数のシンボルについて、それぞれ１つづつテーブルを生成する。

    ARQ,BAL,ALM
    """
    symbols = ["ARQ", "BAL", "ALM"]
    return [
        factory_table_bar_alpaca(symbol=symbol)
        for symbol in symbols
    ]
