import pytest
from alpaca.data.models import BarSet

from tests.utils.factory.infra.api.alpaca import generate_barset_alpaca


@pytest.fixture
def mock_get_barset_alpaca_api(monkeypatch):
    """
    通信をモックし、ダミーのBarSetを返す。
    """
    def _mock_get_barset_alpaca_api(*args, **kwargs):
        return generate_barset_alpaca()

    monkeypatch.setattr(
        'infra.api.alpaca.historical.get_barset_alpaca_api',
        _mock_get_barset_alpaca_api
    )


@pytest.fixture
def mock_get_barset_alpaca_api_empty(monkeypatch):
    """
    通信をモックし、空のBarSetを返す。
    """
    def _mock_get_barset_alpaca_api(*args, **kwargs):
        return BarSet(raw_data={'NOSYMBOL': []})

    monkeypatch.setattr(
        'infra.api.alpaca.historical.get_barset_alpaca_api',
        _mock_get_barset_alpaca_api
    )