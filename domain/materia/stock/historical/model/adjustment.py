from enum import Enum

from alpaca.data.requests import Adjustment as AdjustmentAlpaca

from infra.db.peewee.table.bar import TableBarAlpaca


class Adjustment(Enum):
    """
    株価データの調整方法を表す。

        * RAW: 未調整の生データ。株式分割や配当などの企業アクションによる影響が反映されていない。
        * SPLIT: 株式分割のみ調整済み。株価と出来高が株式分割に応じて調整されている。
        * DIVIDEND: 配当のみ調整済み。過去の配当金額が株価から差し引かれている。
        * ALL: すべての調整が適用済み。株式分割と配当の両方が反映されており、長期的な価格比較に適している。

    これらの調整は、異なる時点の株価を正確に比較するために使用される。
    例えば、株式分割後に株価が半分になった場合、SPLIT調整済みデータでは
    分割前の株価も半分に調整されるため、連続的な価格推移を見ることができる。
    """
    RAW = 'R'
    SPLIT = 'S'
    DIVIDEND = 'D'
    ALL = 'A'


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

