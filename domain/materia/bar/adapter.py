from typing import List

from alpaca.data.requests import Adjustment as AdjustmentAlpaca
from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.bar.model import Adjustment, Bar, Chart, Timeframe
from infra.api.alpaca.historical import Bar as BarAlpacaApi
from infra.db.peewee.table.bar import TableBarAlpaca


def arrive_bar_from_alpaca_api(bar_alpaca_api: BarAlpacaApi) -> Bar:
    """
    Bar:
        Alpaca API -> Domain
    """
    return Bar(
        timestamp=bar_alpaca_api.timestamp,
        open=bar_alpaca_api.open,
        high=bar_alpaca_api.high,
        low=bar_alpaca_api.low,
        close=bar_alpaca_api.close,
        volume=bar_alpaca_api.volume,
        trade_count=bar_alpaca_api.trade_count,
        vwap=bar_alpaca_api.vwap,
    )


def arrive_chart_from_alpaca_api_list(
        bars_alpaca_api: List[BarAlpacaApi],
        adjustment: Adjustment,
        timeframe: Timeframe
) -> Chart:
    """
    Chart:
        AlpacaAPI<List> -> Domain
    """
    bars = [arrive_bar_from_alpaca_api(bar) for bar in bars_alpaca_api]
    symbol = bars_alpaca_api[0].symbol
    return Chart(
        symbol=symbol,
        timeframe=timeframe,
        adjustment=adjustment,
        bars=bars
    )


def arrive_bar_from_peewee_table(bar_peewee_table: TableBarAlpaca) -> Bar:
    """
    Bar:
        PeeweeTable -> Domain
    """
    return Bar(
        timestamp=bar_peewee_table.timestamp,
        open=bar_peewee_table.open,
        high=bar_peewee_table.high,
        low=bar_peewee_table.low,
        close=bar_peewee_table.close,
        volume=bar_peewee_table.volume,
        trade_count=bar_peewee_table.trade_count,
        vwap=bar_peewee_table.vwap,
    )

def arrive_timeframe_from_peewee_table(bar_peewee_table: TableBarAlpaca) -> Timeframe:
    """
    PeeweeTable -> Timeframe
    """
    mapping = {
        1: Timeframe.MIN,
        2: Timeframe.HOUR,
        4: Timeframe.DAY,
        8: Timeframe.WEEK,
        16: Timeframe.MONTH,
    }
    return mapping[bar_peewee_table.timeframe]


def arrive_adjustment_from_peewee_table(bar_peewee_table: TableBarAlpaca) -> Adjustment:
    """
    PeeweeTable -> Domain
    """
    mapping = {
        1: Adjustment.RAW,
        2: Adjustment.SPLIT,
        4: Adjustment.DIVIDEND,
        8: Adjustment.ALL,
    }
    return mapping[bar_peewee_table.adjustment]


def arrive_chart_from_peewee_table(bars_peewee_table: List[TableBarAlpaca]) -> Chart:
    """
    Chart:
        PeeweeTable<List> -> Domain
    """
    symbol = bars_peewee_table[0].symbol
    timeframe = arrive_timeframe_from_peewee_table(bars_peewee_table[0])
    adjustment = arrive_adjustment_from_peewee_table(bars_peewee_table[0])
    bars = [arrive_bar_from_peewee_table(bar) for bar in bars_peewee_table]
    return Chart(
        symbol=symbol,
        timeframe=timeframe,
        adjustment=adjustment,
        bars=bars
    )


def depart_timeframe_to_alpaca_api(timeframe: Timeframe) -> TimeFrameAlpaca:
    """
    Timeframe:
        Domain -> Alpaca API
    """
    timeframe_map = {
        Timeframe.MIN: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Minute),
        Timeframe.HOUR: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Hour),
        Timeframe.DAY: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Day),
        Timeframe.WEEK: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Week),
        Timeframe.MONTH: TimeFrameAlpaca(amount=1, unit=TimeFrameUnit.Month)
    }
    if timeframe not in timeframe_map:
        raise ValueError(
            f"無効なTimeframe: {timeframe}。"
            f"サポートされているTimeframeは "
            f"{', '.join(map(str, timeframe_map.keys()))} です。"
        )
    return timeframe_map[timeframe]


def depart_adjustment_to_alpaca_api(adjustment: Adjustment) -> AdjustmentAlpaca:
    """
    Adjustment:
        Domain -> Alpaca API
    """
    adjustment_map = {
        Adjustment.RAW: AdjustmentAlpaca.RAW,
        Adjustment.SPLIT: AdjustmentAlpaca.SPLIT,
        Adjustment.DIVIDEND: AdjustmentAlpaca.DIVIDEND,
        Adjustment.ALL: AdjustmentAlpaca.ALL,
    }
    if adjustment not in adjustment_map:
        raise ValueError(
            f"無効なAdjustment: {adjustment}。"
            f"サポートされているAdjustmentは "
            f"{', '.join(map(str, adjustment_map.keys()))} です。"
        )
    return adjustment_map[adjustment]


def depart_timeframe_to_peewee_table(timeframe: Timeframe) -> int:
    """
    Timeframe:
        Domain -> PeeweeTable

    注意: TableBarAlpacaの定義を参照する事。
    """
    mapping = {
        Timeframe.MIN: 1,
        Timeframe.HOUR: 2,
        Timeframe.DAY: 4,
        Timeframe.WEEK: 8,
        Timeframe.MONTH: 16,
    }
    if timeframe not in mapping:
        raise ValueError(
            f"無効なTimeframe: {timeframe}。"
            f"サポートされているTimeframeは "
            f"{', '.join(map(str, mapping.keys()))} です。"
        )
    return mapping[timeframe]


def depart_adjustment_to_peewee_table(adjustment: Adjustment) -> int:
    """
    Adjustment:
        Domain -> PeeweeTable

    注意: TableBarAlpacaの定義を参照する事。
    """
    mapping = {
        Adjustment.RAW: 1,
        Adjustment.SPLIT: 2,
        Adjustment.DIVIDEND: 4,
        Adjustment.ALL: 8,
    }
    if adjustment not in mapping:
        raise ValueError(
            f"無効なAdjustment: {adjustment}。"
            f"サポートされているAdjustmentは "
            f"{', '.join(map(str, mapping.keys()))} です。"
        )
    return mapping[adjustment]


def depart_bar_to_peewee_table(
        bar: Bar,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment
) -> TableBarAlpaca:
    """
    Bar:
        Domain -> PeeweeTable
    """
    return TableBarAlpaca(
        symbol=symbol,
        timestamp=bar.timestamp,
        timeframe=depart_timeframe_to_peewee_table(timeframe),
        adjustment=depart_adjustment_to_peewee_table(adjustment),
        open=bar.open,
        high=bar.high,
        low=bar.low,
        close=bar.close,
        volume=bar.volume,
        vwap=bar.vwap,
    )


def depart_chart_to_peewee_table_list(chart: Chart) -> List[TableBarAlpaca]:
    """
    Chart -> PeeweeTable<List>
    """
    return [
        depart_bar_to_peewee_table(bar, chart.symbol, chart.timeframe, chart.adjustment)
        for bar in chart.bars
    ]
