from alpaca.data.models import BarSet

from tests.utils.factory.alpaca import generate_barset, make_barset_from_dict
from tests.utils.mock.loader import load


def test_make_barset_from_dict():
    data = load('barset.json')
    barset = make_barset_from_dict(data)
    assert isinstance(barset, BarSet)