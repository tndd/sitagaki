import pytest
from alpaca.data.enums import Adjustment as AdjustmentAlpaca

from domain.materia.stock.chart.const import Adjustment
from infra.adapter.materia.stock.chart.adjustment import (
    arrive_adjustment_from_table,
    depart_adjustment_to_alpaca_api,
    depart_adjustment_to_table,
)
from infra.db.peewee.table.alpaca.bar import AdjustmentTable
from tests.utils.factory.infra.db.peewee.bar import generate_table_bar_alpaca


def test_arrive_adjustment_from_table():
    """
    bar_table => Adjustment

    adjustmentがrawであることが期待できる。
    """
    bar_table = generate_table_bar_alpaca()
    adjustment = arrive_adjustment_from_table(bar_table)
    assert isinstance(adjustment, Adjustment)
    assert adjustment == Adjustment.RAW


@pytest.mark.parametrize("domain_adjustment, expected_alpaca_adjustment", [
    (Adjustment.RAW, AdjustmentAlpaca.RAW),
    (Adjustment.SPLIT, AdjustmentAlpaca.SPLIT),
    (Adjustment.DIVIDEND, AdjustmentAlpaca.DIVIDEND),
    (Adjustment.ALL, AdjustmentAlpaca.ALL),
])
def test_depart_adjustment_to_alpaca_api(domain_adjustment, expected_alpaca_adjustment):
    assert depart_adjustment_to_alpaca_api(domain_adjustment) == expected_alpaca_adjustment


def test_depart_adjustment_to_table():
    assert depart_adjustment_to_table(Adjustment.RAW) == AdjustmentTable.RAW
    assert depart_adjustment_to_table(Adjustment.SPLIT) == AdjustmentTable.SPLIT
    assert depart_adjustment_to_table(Adjustment.DIVIDEND) == AdjustmentTable.DIVIDEND
    assert depart_adjustment_to_table(Adjustment.ALL) == AdjustmentTable.ALL
