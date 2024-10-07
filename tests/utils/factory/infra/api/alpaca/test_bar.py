from alpaca.data.models.bars import Bar, BarSet

from tests.utils.factory.infra.api.alpaca.bar import (
    generate_bar_alpaca,
    generate_bar_alpaca_list,
    generate_barset_alpaca,
)


def test_generate_barset_alpaca():
    barset = generate_barset_alpaca()
    assert isinstance(barset, BarSet)


def test_generate_bar_alpaca():
    bar = generate_bar_alpaca()
    assert isinstance(bar, Bar)


def test_generate_bar_alpaca_list():
    bars = generate_bar_alpaca_list()
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)