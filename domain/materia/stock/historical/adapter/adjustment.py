from alpaca.data.requests import Adjustment as AdjustmentAlpaca

from domain.materia.stock.historical.model import Adjustment
from infra.db.peewee.table.bar import TableBarAlpaca


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