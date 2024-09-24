from domain.materia.bar.model import Bar
from infra.adapter.materia.bar.arrive import (
    arrive_bar_from_alpaca_api,
    arrive_bar_from_peewee_table,
    arrive_bar_list_from_alpaca_api,
    arrive_bar_list_from_peewee_table,
)
from tests.utils.factory.infra.api.alpaca import generate_bar_alpaca


def test_arrive_bar_from_alpaca_api():
    bar_alpaca_api = generate_bar_alpaca()
    bar = arrive_bar_from_alpaca_api(bar_alpaca_api)
    assert isinstance(bar, Bar)


def test_arrive_bar_list_from_alpaca_api():
    # TODO: 実装
    pass


def test_arrive_bar_from_peewee_table():
    # TODO: 実装
    pass


def test_arrive_bar_list_from_peewee_table():
    # TODO: 実装
    pass
