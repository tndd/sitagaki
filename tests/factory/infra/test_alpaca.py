from alpaca.data.models.bars import BarSet

from tests.utils.factory.infra.api.alpaca import generate_barset


def test_generate_barset():
    barset = generate_barset()
    assert isinstance(barset, BarSet)