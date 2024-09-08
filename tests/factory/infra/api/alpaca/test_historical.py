from alpaca.data.models.bars import Bar, BarSet

from tests.utils.factory.infra.api.alpaca import (
    generate_bar_alpaca,
    generate_barset_alpaca,
)


def test_generate_barset_alpaca():
    barset = generate_barset_alpaca()
    assert isinstance(barset, BarSet)


def test_generate_bar_alpaca():
    bar = generate_bar_alpaca()
    assert isinstance(bar, Bar)