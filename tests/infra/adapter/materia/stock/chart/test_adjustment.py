from alpaca.data.requests import Adjustment as AdjustmentAlpaca

from domain.materia.stock.chart.model import Adjustment
from infra.adapter.materia.stock.chart.adjustment import (
    arrive_adjustment_from_peewee_table,
    depart_adjustment_to_alpaca_api,
    depart_adjustment_to_peewee_table,
)
from tests.utils.mock.infra.db.peewee.bar import generate_table_bar_alpaca


def test_arrive_adjustment_from_peewee_table():
    """
    bar_peewee_table => Adjustment

    adjustmentがrawであることが期待できる。
    """
    bar_peewee_table = generate_table_bar_alpaca()
    adjustment = arrive_adjustment_from_peewee_table(bar_peewee_table)
    assert isinstance(adjustment, Adjustment)
    assert adjustment == Adjustment.RAW


def test_depart_adjustment_to_alpaca_api():
    assert depart_adjustment_to_alpaca_api(Adjustment.RAW) == AdjustmentAlpaca.RAW
    assert depart_adjustment_to_alpaca_api(Adjustment.SPLIT) == AdjustmentAlpaca.SPLIT
    assert depart_adjustment_to_alpaca_api(Adjustment.DIVIDEND) == AdjustmentAlpaca.DIVIDEND
    assert depart_adjustment_to_alpaca_api(Adjustment.ALL) == AdjustmentAlpaca.ALL


def test_depart_adjustment_to_peewee_table():
    assert depart_adjustment_to_peewee_table(Adjustment.RAW) == 1
    assert depart_adjustment_to_peewee_table(Adjustment.SPLIT) == 2
    assert depart_adjustment_to_peewee_table(Adjustment.DIVIDEND) == 4
    assert depart_adjustment_to_peewee_table(Adjustment.ALL) == 8