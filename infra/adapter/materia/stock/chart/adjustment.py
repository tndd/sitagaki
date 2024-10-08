from alpaca.data.enums import Adjustment as AdjustmentAlpaca

from domain.materia.stock.chart.const import Adjustment
from infra.db.peewee.table.alpaca.bar import AdjustmentTable, TableBarAlpaca


def arrive_adjustment_from_table(bar_table: TableBarAlpaca) -> Adjustment:
    """
    PeeweeTable -> Domain
    """
    mapping = {
        AdjustmentTable.RAW: Adjustment.RAW,
        AdjustmentTable.SPLIT: Adjustment.SPLIT,
        AdjustmentTable.DIVIDEND: Adjustment.DIVIDEND,
        AdjustmentTable.ALL: Adjustment.ALL,
    }
    return mapping[bar_table.adjustment]


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


def depart_adjustment_to_table(adjustment: Adjustment) -> AdjustmentTable:
    """
    Adjustment:
        Domain -> PeeweeTable

    注意: TableBarAlpacaの定義を参照する事。
    """
    mapping = {
        Adjustment.RAW: AdjustmentTable.RAW,
        Adjustment.SPLIT: AdjustmentTable.SPLIT,
        Adjustment.DIVIDEND: AdjustmentTable.DIVIDEND,
        Adjustment.ALL: AdjustmentTable.ALL,
    }
    if adjustment not in mapping:
        raise ValueError(
            f"無効なAdjustment: {adjustment}。"
            f"サポートされているAdjustmentは "
            f"{', '.join(map(str, mapping.keys()))} です。"
        )
    return mapping[adjustment]