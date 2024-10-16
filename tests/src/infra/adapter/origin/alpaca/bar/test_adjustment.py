import pytest
from alpaca.data.enums import Adjustment as AdjustmentAlpaca

from fixture.infra.db.peewee.table.alpaca.bar import factory_table_bar_alpaca
from src.domain.origin.alpaca.bar.const import Adjustment
from src.infra.adapter.origin.alpaca.bar.adjustment import (
    arrive_adjustment_from_table,
    depart_adjustment_to_alpaca_api,
    depart_adjustment_to_table,
)
from src.infra.db.peewee.table.alpaca.bar import AdjustmentTable


def test_arrive_adjustment_from_table():
    """
    bar_table => Adjustment

    adjustmentがrawであることが期待できる。
    """
    bar_table = factory_table_bar_alpaca()
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


@pytest.mark.parametrize("domain_adjustment, expected_table_adjustment", [
    (Adjustment.RAW, AdjustmentTable.RAW),
    (Adjustment.SPLIT, AdjustmentTable.SPLIT),
    (Adjustment.DIVIDEND, AdjustmentTable.DIVIDEND),
    (Adjustment.ALL, AdjustmentTable.ALL),
])
def test_depart_adjustment_to_table(domain_adjustment, expected_table_adjustment):
    assert depart_adjustment_to_table(domain_adjustment) == expected_table_adjustment