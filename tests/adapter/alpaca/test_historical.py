from domain.materia.bar.model import Bar
from infra.adapter.alpaca.historical import adapt_to_bar_list
from tests.utils.factory.alpaca import generate_barset
from tests.utils.mock.loader import load


def test_adapt_to_bar_list():
    mock_barset = generate_barset()
    print(mock_barset)
    bars = adapt_to_bar_list(mock_barset)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)