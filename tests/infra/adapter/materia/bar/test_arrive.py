from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar.depart import (
    depart_bar_list_to_peewee_table,
    depart_bar_to_peewee_table,
    depart_timeframe_to_alpaca_api,
)


def test_depart_timeframe_to_alpaca_api():
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.MIN), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.HOUR), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.DAY), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.WEEK), TimeFrameAlpaca)
    assert isinstance(depart_timeframe_to_alpaca_api(Timeframe.MONTH), TimeFrameAlpaca)


def test_depart_bar_to_peewee_table():
    # TODO: 実装
    pass


def test_depart_bar_list_to_peewee_table():
    # TODO: 実装
    pass
