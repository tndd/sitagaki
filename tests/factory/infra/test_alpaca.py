from tests.utils.factory.infra.api.alpaca import (MockBarSet, generate_barset_mock,
                                        make_barset_mock_from_dict)
from tests.utils.mock.loader import load


def test_make_barset_from_dict():
    data = load('barset.json')
    barset = make_barset_mock_from_dict(data)
    assert isinstance(barset, MockBarSet)


def test_generate_barset():
    barset = generate_barset_mock()
    assert isinstance(barset, MockBarSet)