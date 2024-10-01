from datetime import datetime
from typing import Optional

from domain.materia.finance.chart.model import Adjustment, Chart, Timeframe
from domain.materia.finance.chart.repository import ChartRepository


def fetch_chart(
        rp: ChartRepository,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment
    ) -> Chart:
    """
    指定された条件のチャートデータを取得する。
    取得元はまずDBを探し、なければonlineから取得する。
    """
    # まずデータを最新にする
    update_chart(rp, symbol, timeframe, adjustment)
    # データの取得
    return rp.fetch_chart_from_local(symbol, timeframe, adjustment)


def update_chart(
        rp: ChartRepository,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment
    ) -> None:
    """
    指定された条件でonline上から取得したチャートデータで、
    DB上のデータを更新する。

    DB上にある最新のtimestamp~可能な限り直近のデータ。
    """
    # 最新のtimestampを取得
    latest_timestamp = rp.fetch_latest_timestamp_of_symbol(symbol, timeframe, adjustment)
    # それ以降のデータで更新
    rp.store_chart_from_online(symbol, timeframe, adjustment, latest_timestamp)
