from alpaca.data.models.bars import Bar, BarSet

from tests.utils.factory.infra.api.alpaca import generate_bar, generate_barset


def test_generate_barset():
    barset = generate_barset()
    assert isinstance(barset, BarSet)


def test_generate_bar():
    bar = generate_bar()
    assert isinstance(bar, Bar)